package main

import (
	"fmt"
	"os"
	"text/scanner"

	"github.com/sacOO7/socketcluster-client-go/scclient"
)

func onConnect(client scclient.Client) {
	fmt.Println("Connected to server")
}

func onDisconnect(client scclient.Client, err error) {
	fmt.Printf("Error: %s\n", err.Error())
}

func onConnectError(client scclient.Client, err error) {
	fmt.Printf("Error: %s\n", err.Error())
}

func onSetAuthentication(client scclient.Client, token string) {
	fmt.Println("Auth token received :", token)

}

func onAuthentication(client scclient.Client, isAuthenticated bool) {
	fmt.Println("Client authenticated :", isAuthenticated)
	go startCode(client)
}

func main() {
	var reader scanner.Scanner
	client := scclient.New("wss://www.emeraldchat.com/cable")
	client.SetAuthToken("user_id=MjE1NTAyNjI%3D--53715d8c0d5a37453895fbf751e8bc4f9056f2fe")
	client.SetBasicListener(onConnect, onConnectError, onDisconnect)
	client.SetAuthenticationListener(onSetAuthentication, onAuthentication)
	go client.Connect()

	fmt.Println("Enter any key to terminate the program")
	reader.Init(os.Stdin)
	reader.Next()
	// os.Exit(0)
}

func startCode(client scclient.Client) {
	// start writing your code from here
	// All emit, receive and publish events
}
