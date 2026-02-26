package crawler

import (
	"bufio"
	"errors"
	"net/http"
	"net/url"
	"strings"
)

func fetch(raw string) (*http.Response, error) {
	// Parse the URL first
	u, err := url.Parse(raw)
	if err != nil {
		return nil, err
	}

	// Ensure scheme exists
	if u.Scheme == "" {
		u.Scheme = "https"
	}

	// If host is still empty (like "example.com/path" without scheme)
	if u.Host == "" {
		// Re-parse assuming https
		u, err = url.Parse("https://" + raw)
		if err != nil {
			return nil, err
		}
	}

	// Build request explicitly (better than http.Get)
	req, err := http.NewRequest("GET", u.String(), nil)
	if err != nil {
		return nil, err
	}

	// Set a User-Agent (important for crawlers)
	req.Header.Set("User-Agent", "MyCrawler/1.0")

	client := &http.Client{}

	return client.Do(req)
}

func getRobotsTxt(baseDom string, hos *Host) error {
	urlRes, err := url.JoinPath(baseDom, "/robots.txt")
	if err != nil {
		return errors.New("Errors resolving robots.txt")
	}
	res, err := http.Get(urlRes)
	if err != nil {
		return errors.New("Error getting robots.txt")
	}
	switch res.StatusCode {
	case 401:
	case 403:
		hos.disallowAll = true
		return nil
	}
	scanner := bufio.NewScanner(res.Body)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" || line[0] == '#' {
			continue
		}
		splitLine := strings.Split(line, ":")
		switch strings.ToLower(splitLine[0]) {
		case "disallow":
			hos.disallowed = append(hos.disallowed, splitLine[1])
		case "allowed":
			hos.allowed = append(hos.disallowed, splitLine[1])
		case "crawl-delay":
			hos.delay = splitLine[1]
		}
	}
	return nil
}
