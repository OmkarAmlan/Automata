const csvDropzone = document.getElementById("csv-dropzone"); 
  
        csvDropzone.addEventListener("dragover", function (event) { 
            event.preventDefault(); 
            csvDropzone.classList.add("dragover"); 
        }); 
  
        csvDropzone.addEventListener("dragleave", function (event) { 
            event.preventDefault(); 
            csvDropzone.classList.remove("dragover"); 
        }); 
  
        csvDropzone.addEventListener("drop", function (event) { 
            event.preventDefault(); 
            csvDropzone.classList.remove("dragover"); 
            const csvFile = event.dataTransfer.files[0]; 
  
            if (csvFile.type === "text/csv" ||  
                csvFile.type === "application/vnd.ms-excel") { 
                alert("csv file has been selected"); 
                handleCsvFile(csvFile); 
            } else { 
                alert("Please drop a CSV file."); 
            } 
        });

