def recurse_search(url, path, depth_level, soup):
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            if href.startswith("/"):
                href = urljoin(url, href)
            if not href.startswith("#"):
                if urlparse(href).netloc == urlparse(url).netloc:
                        if depth_level == 0:
                            return
                        with lock:
                            if url in checked_urls:
                                return
                            checked_urls.add(url)
                        
                        response = requests.get(url)
                        soup= BeautifulSoup(response.text, 'html.parser')
                        images = soup.find_all('img')
                        img_src = get_all_img_src(images, url)
                        
                        threads = []
                        for image in img_src:
                            if image not in photo_download:
                                t = threading.Thread(target=download_img_threaded, args=(image, save_path))
                                threads.append(t)
                                t.start()
                                
                        # Wait for all threads to finish
                        for t in threads:
                            t.join()
                            
                        recurse_search(url, path, depth_level, soup)