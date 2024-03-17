# crawl gpx spider, limit to 10 and store output in json line format file
# new terminal, cd spider
# scrapy crawl gpx -s CLOSESPIDER_PAGECOUNT=10 -o file.jl

import scrapy

class TemperatureSpider(scrapy.Spider):
    name = 'temperature_data'
    start_urls = ['https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt']

    def parse(self, response):
        lines = response.text.split('\n')
        data_lines = lines[5:]  # This might need adjustment based on the actual number of header lines

        for line in data_lines:
            if line.strip():  # Ensure the line is not empty
                parts = line.split()
                # Extract year, no smoothing, and Lowess(5) values
                if len(parts) >= 3:  # Ensure the line has enough parts to extract
                    year = parts[0]
                    no_smoothing = parts[1]
                    lowess_5 = parts[2]
                    yield {
                        'year': year,
                        'no_smoothing': no_smoothing,
                        'lowess_5': lowess_5
                    }
