function getTimeZone() {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.getElementById('tz').value = timezone;
}
