package crawler

import (
	"fmt"
	"sync"
	"time"
)

type Crawler struct {
	StartDomain      string
	RetriesPerPage   int
	RequestPerSecond int
	Delay            time.Time
}

func (s *Crawler) StartCrawl() {

	var wg sync.WaitGroup
	seenHosts := make(map[string]int)
	hosts := make(chan Host, 100)
	startingHost := Host{
		baseDomain: s.StartDomain,
		subDomains: make([]string, 0),
		seen:       make(map[string]int),
	}

	go func() {
		wg.Wait()
		close(hosts)
	}()

	hosts <- startingHost
	i := 0
	for host := range hosts {
		//skip if already seen
		i++
		if seenHosts[host.baseDomain] == 0 {
			seenHosts[host.baseDomain] = 1
			wg.Add(1)
			go s.crawl(&host, hosts, &wg)
		}
		if i >= 10 {
			break
		}
	}

	wg.Wait()
}

func (s *Crawler) crawl(hos *Host, list chan Host, wg *sync.WaitGroup) {
	defer wg.Done()
	err := getRobotsTxt(hos.baseDomain, hos)
	if err != nil {
		hos.errs = append(hos.errs, err.Error())
	}
	if hos.disallowAll {
		return
	}

	hos.subDomains = append(hos.subDomains, hos.baseDomain)

	for i := 0; i < len(hos.subDomains); i++ {
		//temporary break - only crawl first 30 pages of a host
		if i > 30 {
			break
		}

		time.Sleep(time.Second) //add * craw delay logic
		domain := hos.subDomains[i]
		hos.seen[domain] += 1

		resp, err := fetch(domain)
		if err != nil {
			fmt.Printf("Error in get request: %s", err.Error())
			hos.errs = append(hos.errs, err.Error())
			continue
		}

		//check status code
		if resp.StatusCode != 200 {
			fmt.Printf("Bad Status code from: %s \n", domain)
			continue
		}

		//get all href's
		links := getLinksFromHTML(resp)
		if links == nil {
			fmt.Printf("No links grabbed for %s \n", domain)
			continue
		}

		//determine if subdomain has been seen and determine if new host
		//append new domains to list
		for i, url := range links {
			//only grab the first 10 links from a page
			if i > 10 {
				break
			}
			if hos.seen[url] > 0 {
				fmt.Printf("Seen URL %s, %d \n", url, hos.seen[url])
				continue
			}
			//if new host then create a new host and add to channel then finish ittr
			new, newbase := isNewHost(hos.baseDomain, url)
			if new {
				fmt.Printf("New host: %s \n", newbase)
				newHost := Host{
					baseDomain: newbase,
					subDomains: make([]string, 0),
					seen:       make(map[string]int),
				}
				list <- newHost
				continue
			}
			//check if in disallowed
			hos.subDomains = append(hos.subDomains, url)

		}

		resp.Body.Close()
	}

}
