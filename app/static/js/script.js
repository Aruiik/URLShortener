
async function copyLink(link) {
    try {
        await navigator.clipboard.writeText(link);

        alert("Link został skopiowany!");
    } catch (error) {
        alert("Nie udało się skopiować linku.");
    }
}
