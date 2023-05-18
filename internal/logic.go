package logic

type Game struct {
	Board         [15][15]string
	CurrentPlayer string
	Players       [2]string
	Status        string
}

func NewEmptyGame() *Game {
	return &Game{
		Board:         [15][15]string{},
		CurrentPlayer: "white",
		Players:       [2]string{"", ""},
		Status:        "waiting",
	}
}
