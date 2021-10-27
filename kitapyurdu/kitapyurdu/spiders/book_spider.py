import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    book_count = 1
    file = open("books.txt","a",encoding = "UTF-8")
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1"
    ]



    def parse(self, response):
        book_names =  response.css("div.name.ellipsis a span::text").extract()
        authors = response.css("div.author span a span::text").extract()
        publishers = response.css("div.publisher span a span::text").extract()


        for i in range(len(book_names)):
            self.file.write(str(self.book_count) + ": **************************************************\n")
            self.file.write("Kitap Adı : " + book_names[i] + "\n")
            self.file.write("Yazar : " + authors[i]+ "\n")
            self.file.write("Yayınevi : " + publishers[i] + "\n")
            self.book_count += 1
        next_url = response.css("a.next::attr(href)").get()
        self.page_count += 1

        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url=next_url,callback = self.parse)
        else:
            self.file.close()