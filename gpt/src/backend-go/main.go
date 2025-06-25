// file: backend-go/main.go
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/lib/pq" // PostgreSQL driver
)

// DB connection instance
var db *sql.DB

// Struct to hold the counts for JSON response
type Counts struct {
	GoCount     int `json:"go_count"`
	PythonCount int `json:"python_count"`
}

// initDB connects to the PostgreSQL database.
func initDB() {
	// Get the database connection string from environment variables
	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		log.Fatal("DATABASE_URL environment variable is not set")
	}

	var err error
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error connecting to the database: ", err)
	}

	// Ping the database to ensure the connection is alive
	err = db.Ping()
	if err != nil {
		log.Fatal("Error pinging the database: ", err)
	}
	fmt.Println("Successfully connected to PostgreSQL!")
}

// getCountsHandler fetches the current counts from the database.
func getCountsHandler(w http.ResponseWriter, r *http.Request) {
	var counts Counts
	// We know our data is in the row with id=1
	query := "SELECT golang_requested_counts, python_requested_counts FROM request_counts WHERE id = 1"
	err := db.QueryRow(query).Scan(&counts.GoCount, &counts.PythonCount)
	if err != nil {
		http.Error(w, "Failed to retrieve counts", http.StatusInternalServerError)
		log.Println("Error querying counts:", err)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(counts)
}

// incrementGoCountHandler increments the Go request count in the database.
func incrementGoCountHandler(w http.ResponseWriter, r *http.Request) {
	// We only accept POST requests for this endpoint
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	// Update the count and the timestamp. The a+1 is atomic.
	query := `
		UPDATE request_counts
		SET golang_requested_counts = golang_requested_counts + 1,
		    last_go_request_time = $1
		WHERE id = 1`

	_, err := db.Exec(query, time.Now())
	if err != nil {
		http.Error(w, "Failed to increment Go count", http.StatusInternalServerError)
		log.Println("Error incrementing Go count:", err)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Go count incremented successfully")
}

// corsMiddleware adds CORS headers to allow requests from our React frontend.
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	// Initialize the database connection
	initDB()
	defer db.Close()

	// Create a new ServeMux and register handlers
	mux := http.NewServeMux()
	mux.HandleFunc("/api/counts", getCountsHandler)
	mux.HandleFunc("/api/go/increment", incrementGoCountHandler)

	// Wrap the mux with the CORS middleware
	handler := corsMiddleware(mux)

	// Start the server
	log.Println("Go API server starting on port 8080...")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		log.Fatalf("could not start server: %v", err)
	}
}
