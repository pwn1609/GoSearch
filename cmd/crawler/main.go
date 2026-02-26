package main

import (
	"github.com/pwn1609/GoSearch/internal/crawler"
)

func main() {

	crawler := crawler.Crawler{
		StartDomain: "target.com",
	}
	crawler.StartCrawl()

}
