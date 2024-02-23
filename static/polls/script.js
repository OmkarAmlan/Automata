const csvDropzone = document.getElementById("csv-dropzone");
    const csvFileInput = document.getElementById("csv-file-input");

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
        handleCsvFile(csvFile);
    });

    function browseFiles() {
        csvFileInput.click();
    }

    csvFileInput.addEventListener("change", function () {
        const csvFile = csvFileInput.files[0];
        handleCsvFile(csvFile);
    });

    function handleCsvFile(file) {
        if (file.type === "text/csv" || file.type === "application/vnd.ms-excel") {
            alert("CSV file has been selected");
            // Additional logic if needed
        } else {
            alert("Please select a CSV file.");
        }
    }