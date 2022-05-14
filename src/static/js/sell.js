function less() {
    q = document.getElementById('qty')
    v = parseInt(q.value) - 1
    if (v < 0) {
        v = 0
    }
    q.value = v
}

function more() {
    q = document.getElementById('qty')
    v = parseInt(q.value) + 1
    q.value = v
}
