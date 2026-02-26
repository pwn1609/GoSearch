package crawler

import (
	"net/http"
	"net/url"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

func getLinksFromHTML(resp *http.Response) []string {

	urls := make([]string, 0)

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil
	}

	doc.Find("a[href]").Each(func(i int, s *goquery.Selection) {
		href, exists := s.Attr("href")
		if exists {
			href = strings.TrimSpace(href)
			if len(href) == 0 || href[0] == '#' {
				return
			}
			ref, err := url.Parse(href)
			if err != nil {
				return
			}
			abs := resp.Request.URL.ResolveReference(ref)
			urls = append(urls, abs.String())
		}
	})
	return urls
}
