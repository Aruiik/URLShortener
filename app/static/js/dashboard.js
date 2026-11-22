
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("linkSearch");
    const tableBody = document.getElementById("linksTableBody");
    const noResults = document.getElementById("noSearchResults");
    const resultsCounter = document.getElementById("searchResults");

    const sortSelect = document.getElementById("sortSelect");
    const sortDirection = document.getElementById("sortDirection");

    const pageSizeSelect = document.getElementById("pageSize");
    const previousPageButton = document.getElementById("previousPage");
    const nextPageButton = document.getElementById("nextPage");
    const pageInfo = document.getElementById("pageInfo");

    let currentPage = 1;

    const entries = tableBody
        ? Array.from(tableBody.querySelectorAll("[data-link-row]")).map(
            (row) => ({
                row,
                detailsRow: row.nextElementSibling,
            })
        )
        : [];

    // ========================================
    // WYSZUKIWANIE
    // ========================================

    function getFilteredEntries() {
        const query = searchInput
            ? searchInput.value.trim().toLocaleLowerCase("pl")
            : "";

        return entries.filter((entry) => {
            const searchableText = entry.row.dataset.search
                .toLocaleLowerCase("pl");

            return searchableText.includes(query);
        });
    }

    // ========================================
    // SORTOWANIE
    // ========================================

    function sortRows() {
        if (!sortSelect || !sortDirection) {
            return;
        }

        const sortBy = sortSelect.value;
        const direction = sortDirection.dataset.direction;

        entries.sort((a, b) => {
            let comparison = 0;

            if (sortBy === "code") {
                comparison = a.row.dataset.code.localeCompare(
                    b.row.dataset.code,
                    "pl",
                    { numeric: true, sensitivity: "base" }
                );
            }

            if (sortBy === "clicks") {
                comparison =
                    Number(a.row.dataset.clicks) -
                    Number(b.row.dataset.clicks);
            }

            if (sortBy === "created") {
                comparison =
                    Date.parse(a.row.dataset.created) -
                    Date.parse(b.row.dataset.created);
            }

            return direction === "desc"
                ? -comparison
                : comparison;
        });

        // Przenosimy główny wiersz i szczegóły jako jedną parę
        const fragment = document.createDocumentFragment();

        entries.forEach((entry) => {
            fragment.appendChild(entry.row);

            if (entry.detailsRow?.hasAttribute("data-details-row")) {
                fragment.appendChild(entry.detailsRow);
            }
        });

        tableBody.appendChild(fragment);
    }

    // ========================================
    // PAGINACJA I AKTUALIZACJA TABELI
    // ========================================

    function updateTable() {
        if (!tableBody) {
            return;
        }

        const filteredEntries = getFilteredEntries();

        const pageSize = pageSizeSelect
            ? Number(pageSizeSelect.value)
            : 10;

        const totalEntries = filteredEntries.length;
        const totalPages = Math.max(1, Math.ceil(totalEntries / pageSize));

        // Zabezpieczenie przed wyjściem poza zakres stron
        currentPage = Math.min(currentPage, totalPages);

        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = startIndex + pageSize;

        const visibleEntries = filteredEntries.slice(
            startIndex,
            endIndex
        );

        const visibleSet = new Set(visibleEntries);

        entries.forEach((entry) => {
            const matchesSearch = filteredEntries.includes(entry);
            const isOnCurrentPage = visibleSet.has(entry);

            entry.row.hidden = !isOnCurrentPage;

            if (entry.detailsRow?.hasAttribute("data-details-row")) {
                entry.detailsRow.hidden = !isOnCurrentPage;
            }

            // Zamykamy szczegóły linków, które nie pasują do wyszukiwania
            if (!matchesSearch) {
                entry.detailsRow?.classList.remove("expanded");

                const toggleButton = entry.row.querySelector(
                    "[data-details-toggle]"
                );

                if (toggleButton) {
                    toggleButton.setAttribute("aria-expanded", "false");
                    toggleButton.classList.remove("expanded");
                }
            }
        });

        // Licznik wyników wyszukiwania
        if (resultsCounter) {
            resultsCounter.textContent =
                `Znaleziono ${totalEntries} linków`;
        }

        // Komunikat o braku wyników
        if (noResults) {
            noResults.hidden = totalEntries !== 0;
        }

        // Informacje o aktualnej stronie
        if (pageInfo) {
            pageInfo.textContent =
                `Strona ${currentPage} z ${totalPages}`;
        }

        // Przyciski nawigacyjne
        if (previousPageButton) {
            previousPageButton.disabled = currentPage <= 1;
        }

        if (nextPageButton) {
            nextPageButton.disabled = currentPage >= totalPages;
        }
    }

    // ========================================
    // OBSŁUGA WYSZUKIWANIA
    // ========================================

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            currentPage = 1;
            updateTable();
        });
    }

    // ========================================
    // OBSŁUGA SORTOWANIA
    // ========================================

    if (sortSelect) {
        sortSelect.addEventListener("change", () => {
            currentPage = 1;
            sortRows();
            updateTable();
        });
    }

    if (sortDirection) {
        sortDirection.addEventListener("click", () => {
            const currentDirection = sortDirection.dataset.direction;

            const newDirection =
                currentDirection === "desc" ? "asc" : "desc";

            sortDirection.dataset.direction = newDirection;

            sortDirection.textContent =
                newDirection === "desc"
                    ? "↓ Malejąco"
                    : "↑ Rosnąco";

            currentPage = 1;
            sortRows();
            updateTable();
        });
    }

    // ========================================
    // OBSŁUGA PAGINACJI
    // ========================================

    if (pageSizeSelect) {
        pageSizeSelect.addEventListener("change", () => {
            currentPage = 1;
            updateTable();
        });
    }

    if (previousPageButton) {
        previousPageButton.addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                updateTable();
            }
        });
    }

    if (nextPageButton) {
        nextPageButton.addEventListener("click", () => {
            currentPage++;
            updateTable();
        });
    }

    // ========================================
    // ROZWIJANIE SZCZEGÓŁÓW
    // ========================================

    document.querySelectorAll("[data-details-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const detailsRow = document.getElementById(
                button.getAttribute("aria-controls")
            );

            if (!detailsRow) {
                return;
            }

            const isExpanded =
                button.getAttribute("aria-expanded") === "true";

            detailsRow.classList.toggle("expanded", !isExpanded);

            button.setAttribute(
                "aria-expanded",
                String(!isExpanded)
            );

            button.classList.toggle("expanded", !isExpanded);
        });
    });

    // ========================================
    // KOPIOWANIE LINKÓW
    // ========================================

    document.querySelectorAll("[data-copy]").forEach((button) => {
        button.addEventListener("click", async () => {
            const text = button.dataset.copy;
            const originalText = button.textContent;

            try {
                await navigator.clipboard.writeText(text);

                button.textContent = "Skopiowano!";
                button.classList.add("copied");

                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove("copied");
                }, 1500);
            } catch (error) {
                console.error("Nie udało się skopiować linku:", error);

                button.textContent = "Błąd";

                setTimeout(() => {
                    button.textContent = originalText;
                }, 1500);
            }
        });
    });

    // Początkowe sortowanie i wyświetlenie tabeli
    sortRows();
    updateTable();
});
