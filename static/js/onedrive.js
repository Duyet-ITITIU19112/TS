document.addEventListener("DOMContentLoaded", function () {
    // Fetch the root folder on initial page load
    fetchFolderContents("root"); // Start by loading the OneDrive main page

    // Attach event listeners for dynamically created elements
    function attachEventListeners() {
        document.querySelectorAll(".folder").forEach(function (folderElement) {
            folderElement.addEventListener("click", function () {
                const folderId = this.getAttribute("data-id");
                navigateToFolder(folderId); // Navigate to the selected folder
            });
        });

        document.querySelectorAll(".file").forEach(function (fileElement) {
            fileElement.addEventListener("click", function () {
                const fileUrl = this.getAttribute("data-url"); // File's direct download/view URL
                const fileName = this.getAttribute("data-name"); // File's name/extension
                const resourceId = this.getAttribute("data-resource-id"); // Resource ID for the file
                const userId = this.getAttribute("data-user-id"); // User ID for OneDrive
        
                const fileExtension = fileName.substring(fileName.lastIndexOf(".")).toLowerCase();
        
                if (fileExtension === ".pdf") {
                    // PDFs: Open directly in the browser
                    window.open(fileUrl, '_blank');
                    console.log("Opening PDF file:", fileUrl);
                } else if ([".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"].includes(fileExtension)) {
                    // Office files: Use OneDrive viewer link
                    if (resourceId && userId) {
                        const viewerUrl = `https://onedrive.live.com/personal/${userId}/_layouts/15/Doc.aspx?resid=${resourceId}&app=Word`;
                        window.open(viewerUrl, '_blank'); // Use the viewer for Office files
                        console.log("Opening Office file in OneDrive viewer:", viewerUrl);
                    } else {
                        console.error("Missing metadata for Office file.");
                    }
                } else {
                    // Unsupported or fallback files: Open/download directly
                    console.log("Opening unsupported file type:", fileUrl);
                    window.open(fileUrl, '_blank'); // Default to opening the raw file URL
                }
            });
        });

        // Search button click listener
        const searchButton = document.getElementById("searchButton");
        searchButton.addEventListener("click", function () {
            const keyword = document.getElementById("searchBar").value.trim().toLowerCase();
            if (keyword) {
                searchFiles(keyword); // Perform search
            } else {
                fetchFolderContents("root"); // Reload root folder if input is empty
            }
        });
    }

    // Fetch folder contents from the backend
    function fetchFolderContents(folderId) {
        if (!folderId || folderId === "folder_id") {
            folderId = "root"; // Default to the root folder
        }

        console.log("Fetching folder contents for:", folderId);

        const fileList = document.getElementById("fileList");
        fileList.innerHTML = '<li>Loading...</li>'; // Display loading message

        // Fetch folder contents
        fetch(`/api/onedrive/folder/${encodeURIComponent(folderId)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP Error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                renderFileList(data); // Render the folder contents
            })
            .catch(error => {
                console.error("Error fetching folder contents:", error);
                fileList.innerHTML = '<li>Failed to load contents. Please try again.</li>';
            });
    }

    // Function to render file and folder list
    function renderFileList(data) {
        const fileList = document.getElementById("fileList");
        fileList.innerHTML = ""; // Clear the current list

        data.forEach(item => {
            const listItem = document.createElement("li");
            if (item.folder) {
                listItem.innerHTML = `📁 <span class="folder" data-id="${item.id}">${item.name}</span>`;
            } else {
                listItem.innerHTML = `📄 <span 
                    class="file" 
                    data-url="${item['@microsoft.graph.downloadUrl']}" 
                    data-name="${item.name}" 
                    data-resource-id="${item.id}" 
                    data-user-id="C693C1CC92EF379F">${item.name}</span>`;
            }
            fileList.appendChild(listItem);
        });

        attachEventListeners(); // Reattach listeners for newly added content
    }

    // Navigate to the selected folder
    function navigateToFolder(folderId) {
        history.pushState({ folderId: folderId }, null, `/folder/${folderId}`); // Update browser history
        fetchFolderContents(folderId); // Fetch contents of the selected folder
    }

    // Search for files by keyword
    function searchFiles(keyword) {
        const fileList = document.getElementById("fileList");
        const allFiles = document.querySelectorAll(".file"); // Get all files
        fileList.innerHTML = ""; // Clear the current list

        allFiles.forEach(file => {
            const fileName = file.getAttribute("data-name").toLowerCase();
            const fileExtension = fileName.substring(fileName.lastIndexOf(".")).toLowerCase();

            // Match files by keyword and extension
            if (fileName.includes(keyword) && [".doc", ".docx"].includes(fileExtension)) {
                const clonedFile = file.parentElement.cloneNode(true);
                fileList.appendChild(clonedFile);
            }
        });

        if (fileList.innerHTML === "") {
            fileList.innerHTML = "<li>No matching files found.</li>"; // Display if no matches
        }
    }

    // Handle browser back/forward navigation
    window.addEventListener("popstate", function (event) {
        if (event.state && event.state.folderId) {
            console.log("Navigating to folder from history:", event.state.folderId);
            fetchFolderContents(event.state.folderId); // Load folder contents
        } else {
            const currentPath = window.location.pathname;

            // Handle navigation back to the main page (root directory)
            if (currentPath === "/onedrive" || currentPath === "/") {
                console.log("Back to main OneDrive page");
                fetchFolderContents("root"); // Reload the main page
            } else {
                console.error("Unknown path:", currentPath); // Log unexpected paths
            }
        }
    });

    attachEventListeners(); // Attach listeners on page load
});
