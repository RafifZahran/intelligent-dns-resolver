package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"
	"time"
)

type Student struct {
	StudentID    string `json:"student_id"`
	Name         string `json:"name"`
	StudyProgram string `json:"study_program"`
}

var (
	studentsDB = make(map[string]Student)
	dbMutex    sync.RWMutex
)

func studentHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	switch r.Method {
	case http.MethodPost:

		var newStudent Student
		err := json.NewDecoder(r.Body).Decode(&newStudent)
		if err != nil || newStudent.StudentID == "" {
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}

		dbMutex.Lock()
		studentsDB[newStudent.StudentID] = newStudent
		dbMutex.Unlock()

		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Student data saved successfully")

	case http.MethodGet:

		studentID := r.URL.Query().Get("id")

		if studentID != "" {

			dbMutex.RLock()
			student, exists := studentsDB[studentID]
			dbMutex.RUnlock()

			if !exists {

				http.Error(w, "Student not found", http.StatusNotFound)
				return
			}
			json.NewEncoder(w).Encode(student)
		} else {

			dbMutex.RLock()
			var allStudents []Student
			for _, s := range studentsDB {
				allStudents = append(allStudents, s)
			}
			dbMutex.RUnlock()

			json.NewEncoder(w).Encode(allStudents)
		}

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func startServer() {
	http.HandleFunc("/student", studentHandler)
	log.Println("Server is running on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}

func main() {

	go startServer()

	time.Sleep(1 * time.Second)
	fmt.Println("\n--- Memulai Simulasi HTTP Client ---\n")

	newStudent := Student{
		StudentID:    "2812345678",
		Name:         "Joko Satrio",
		StudyProgram: "Computer Science",
	}

	fmt.Println("Step 1: Client sends POST request /student")
	jsonData, _ := json.Marshal(newStudent)
	respPost, err := http.Post("http://localhost:8080/student", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatalf("Error sending POST request: %v", err)
	}
	defer respPost.Body.Close()

	bodyPost, _ := io.ReadAll(respPost.Body)
	fmt.Printf("Step 2: Server response (Status: %d): %s\n\n", respPost.StatusCode, string(bodyPost))

	fmt.Println("Step 3: Client sends GET request /student (Retrieve All)")
	respGetAll, err := http.Get("http://localhost:8080/student")
	if err != nil {
		log.Fatalf("Error sending GET request: %v", err)
	}
	defer respGetAll.Body.Close()

	bodyGetAll, _ := io.ReadAll(respGetAll.Body)
	fmt.Printf("Step 4: Server returns all student data (Status: %d):\n%s\n\n", respGetAll.StatusCode, formatJSON(bodyGetAll))

	targetID := "2812345678"
	fmt.Printf("Step 5: Client sends GET request /student?id=%s (Retrieve Selected)\n", targetID)
	respGetOne, err := http.Get("http://localhost:8080/student?id=" + targetID)
	if err != nil {
		log.Fatalf("Error sending GET request: %v", err)
	}
	defer respGetOne.Body.Close()

	bodyGetOne, _ := io.ReadAll(respGetOne.Body)
	fmt.Printf("Step 6: Server returns selected item (Status: %d):\n%s\n\n", respGetOne.StatusCode, formatJSON(bodyGetOne))

	fmt.Println("Step Extra: Client sends GET request for unknown ID (Testing 404)")
	respGet404, _ := http.Get("http://localhost:8080/student?id=9999999999")
	defer respGet404.Body.Close()
	body404, _ := io.ReadAll(respGet404.Body)
	fmt.Printf("Server response for unknown ID (Status: %d): %s\n", respGet404.StatusCode, string(body404))
}

func formatJSON(data []byte) string {
	var prettyJSON bytes.Buffer
	if err := json.Indent(&prettyJSON, data, "", "  "); err != nil {
		return string(data)
	}
	return prettyJSON.String()
}
