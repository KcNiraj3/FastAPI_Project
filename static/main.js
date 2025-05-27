document.getElementById('taskForm').addEventListener('submit', async function(e) {
        e.preventDefault(); //Submit the form and reload the entire page, prevents the browser's default form behavior
      
        const task = {
          title: document.getElementById('title').value,
          description: document.getElementById('description').value,
          is_completed: document.getElementById('is_completed').checked
        };
      
        //fetch() sends the data to the FastAPI backend.
        const response = await fetch("http://127.0.0.1:8000/tasks/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify([task])  // Note: you're posting a list of tasks, converts a JavaScript object (or array) into a JSON string
          //body: JSON.stringify(task)       // for one task
          //body: JSON.stringify([task])     // for a list of tasks
          //body refers to the data you're sending to the FastAPI backend 
        });
        // Clear form after post in UI
        //document.getElementById("taskForm").reset();
        if (response.ok) {
          alert("Task created!");
          this.reset();
        } else {
          alert("Error creating task");
        }
      
        const result = await response.json(); //JSON string into a usable JavaScript object
        console.log(result);

        
      });