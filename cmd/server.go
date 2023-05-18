package main

import (
	"fmt"
	"net"

	logic "github.com/czmatejt9/simple_online_gomoku/internal"
)

type Message struct {
	from    string
	payload []byte
}

type Server struct {
	listenAddr string
	ln         net.Listener
	quitch     chan struct{}
	msgch      chan Message
}

func NewServer(listenAddr string) *Server {
	return &Server{
		listenAddr: listenAddr,
		quitch:     make(chan struct{}),
		msgch:      make(chan Message, 16),
	}
}

func (s *Server) Start() error {
	ln, err := net.Listen("tcp", s.listenAddr)
	fmt.Println("server started")
	if err != nil {
		return err
	}

	defer ln.Close()
	s.ln = ln

	go s.AcceptLoop()

	<-s.quitch
	close(s.msgch)

	fmt.Println("server stopped")
	return nil
}

func (s *Server) Stop() {
	close(s.quitch)
	close(s.msgch)
	fmt.Println("server stopped")
}

func (s *Server) AcceptLoop() {
	for {
		conn, err := s.ln.Accept()
		if err != nil {
			fmt.Println("accept error: ", err)
			continue
		}
		fmt.Println("accept: ", conn.RemoteAddr())
		conn.Write([]byte("connected to server"))

		go s.readLoop(conn)
	}
}

func (s *Server) readLoop(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("read error: ", err)
			return
		}

		s.msgch <- Message{
			from:    conn.RemoteAddr().String(),
			payload: buf[:n],
		}
	}

}

func main() {
	s := NewServer(":3000")

	go func() {
		for msg := range s.msgch {
			fmt.Println("Message from ", msg.from, ":", string(msg.payload))
		}
	}()

	a := logic.NewEmptyGame()
	fmt.Printf("%+v\n", a)
	// TODO: implement game logic and remove this later

	s.Start()
}
