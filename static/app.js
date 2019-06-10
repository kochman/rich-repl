function parseResponse(resp) {
    return new Promise((resolve, reject) => {
        resolve(resp.text());
    });
}

document.getElementById("eval-input").addEventListener("keyup", (e) => {
    if (event.keyCode === 13) {
        // grab the input and remove it from the text box
        const input = e.target.value;
        e.target.value = "";

        // submit it to this eval session
        data = { "session_id": window.sessionID, "input": input };
        fetch("/api/evaluate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        }).then(
            parseResponse
        ).then((res) => {
            const inputEl = document.createTextNode(`> ${input}\n`);
            document.getElementById("output").appendChild(inputEl);

            const outputEl = document.createTextNode(`${res}\n`);
            document.getElementById("output").appendChild(outputEl);
        }).catch(() => {
            // put the input back into the text box if there was a problem
            e.target.value = input;
        });
    }
});
