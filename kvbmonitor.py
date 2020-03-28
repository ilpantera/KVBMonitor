#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import datetime
from itertools import islice
from bs4 import BeautifulSoup
import requests
import threading


class KVBMonitorAusgabe(SampleBase):
    def __init__(self, *args, **kwargs):
        super(KVBMonitorAusgabe, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("resources/fonts/5x7.bdf")
        # Definition der Schriftfarbe
        textColor = graphics.Color(255, 255, 255)
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
            "Connection": "close"
        
        }
        
        url = "https://kvb.koeln/qr/632/"

        while True:
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, features="html.parser")
            tables = soup.find_all("table", class_="display")
            departures = []
            for row in tables[0].find_all("tr"):
                tds = row.find_all("td")
                (line_id, direction, wait_time) = (tds[0].text, tds[1].text, tds[2].text)
                line_id = line_id.replace(u"\xa0", "")
                direction = direction.replace(u"\xa0", "")
                if(wait_time == "Sofort"): wait_time = "0 Min"
                wait_time = wait_time.replace(u" Min", "m").strip()
                if(len(wait_time) == 2): wait_time = " {0}".format(wait_time)

                if(wait_time == " 4m"): wait_time = "3+1m"
                if(wait_time == " 9m"): wait_time = "09m"

                try:
                    line_id = int(line_id)
                except:
                    pass
                if(direction == "Bocklemünd" or direction == "Rochusplatz"):
                    departures.append({
                        "line_id": line_id,
                        "direction": direction,
                        "wait_time": wait_time
                    })
            soup.decompose()
            canvas.Clear()

            # Display the current date and time on top
            now = datetime.datetime.now()
            curr_date = now.strftime("%d.%m.")
            curr_time = now.strftime("%H:%M")
            graphics.DrawText(canvas, font, 2, 8, textColor, curr_date)
            graphics.DrawText(canvas, font, 37, 8, textColor, curr_time)
            
            # Set y-position of first connection to 16px
            ymargin = 19

            #Kommandozeilenausgabe aktivieren
            #print("{0}        {1}".format(curr_date, curr_time))

            departures = islice(departures, 2)

            for depart in departures:
                if(depart['direction'] == "Bocklemünd"): depart['direction'] = "Bockl."
                if(depart['direction'] == "Rochusplatz"): depart['direction'] = "Rochu."
                connection = "{0} {1} {2}".format(str(depart['line_id']), depart['direction'], depart['wait_time'])    
                
                #Kommandozeilenausgabe aktivieren
                #print(connection)
                graphics.DrawText(canvas, font, 2, ymargin, textColor, connection)
                ymargin = ymargin + 10

            time.sleep(5) 

# Main function
if __name__ == "__main__":
    KVBMonitor_Ausgabe = KVBMonitorAusgabe()
    if (not KVBMonitor_Ausgabe.process()):
        KVBMonitor_Ausgabe.print_help()
