function generateOutput(res, refs = {}) {
    console.log(res);
    refs[res.id] = res
    if (res.type === "primitive") {
        const container = document.createElement("div");
        const el = document.createTextNode(`${res.value}\n`);
        container.appendChild(el);

        for (const d of res.detected) {
            if (d === "image") {
                const imgEl = document.createElement("img");
                imgEl.src = res.raw;
                container.appendChild(imgEl);
            }
        }

        return container;
    } else if (res.type === "dict") {
        const container = document.createElement("div");

        container.innerText += "{";
        for (const v of res.values) {
            const el = document.createTextNode(`${v.key}: `);
            container.appendChild(el);
            container.appendChild(generateOutput(v), refs);
        }
        container.innerHTML += "}";

        return container;
    } else if (res.type === "reference") {
        const container = document.createElement("span");
        const button = document.createElement("button");
        button.innerHTML = "&darr;";
        button.addEventListener("click", () => {
            console.log("hi");
            container.appendChild(generateOutput(refs[res.value], refs));
        });
        container.appendChild(button);
        return container;
    } else if (res.type === "unknown") {
        const container = document.createElement("div");
        const el = document.createTextNode(`${res.value}\n`);
        container.appendChild(el);
        return container;
    }
    console.error("unknown value type");
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
            (res) => res.json()
        ).then((res) => {
            const inputEl = document.createTextNode(`> ${input}\n`);
            document.getElementById("output").appendChild(inputEl);

            if (res !== null) {
                const outputEl = generateOutput(res);
                document.getElementById("output").appendChild(outputEl);
            }
        }).catch(() => {
            // put the input back into the text box if there was a problem
            e.target.value = input;
        });
    }
});
