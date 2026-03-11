package main

import (
	"github.com/pwn1609/GoSearch/internal/crawler"
)

func main() {

	cfg, err := crawler.LoadConfig("config.yaml")
	if err != nil {
		return
	}

	crawler := crawler.Crawler{
		Config: cfg,
	}
	crawler.StartCrawl()

}
