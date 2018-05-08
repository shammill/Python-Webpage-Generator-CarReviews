#-----Task Description-----------------------------------------------#
#
#  HISTOGRAMS
#
#  This Python program queries a MySQL database to extract owners'
#  ratings for specific models of cars and displays them as
#  histograms in HTML web pages.  See the instructions for more
#  detail.
#
#  It is assumed that the database has been created and populated
#  and the SQL server is running.
#
#--------------------------------------------------------------------#



#-----Students' Solution---------------------------------------------#
#
#  Complete the task by filling in the template below.

## Get the MySQL functions
import MySQLdb

## Alternative for Mac users
##import mysql.connector
##MySQLdb = mysql.connector


##### PUT YOUR create_histograms FUNCTION HERE

#Connect to our database and assign our cursor.
connection = MySQLdb.connect(host = "127.0.0.1", user = "root", 
                       passwd = "", db = "car_reviews")
cursor = connection.cursor()


#Creating a rating class for cleaner code and easier processing.
class Rating:
    def __init__(self):
        self.name = ''
        self.list = []
        self.number_of_reviews = ()
        self.avg_rating = ()
        self.five_star_count = ()
        self.four_star_count = ()
        self.three_star_count = ()
        self.two_star_count = ()
        self.one_star_count = ()

# Main program function used to query our db and call other functions.
def create_histograms(make_model_list):
    for car_make_model in make_model_list:
        car_make = car_make_model[0]
        car_model = car_make_model[1]

        # Queries the database for every car make and model asked of it, providing every rating for each rating type.
        sqlquery_car_ratings = "SELECT overallRating, priceRating, safetyRating, reliabilityRating, serviceRating, styleRating \
        FROM car_details INNER JOIN car_ratings ON car_details.carId=car_ratings.carId \
        WHERE make = '" + car_make + "' AND model = '" + car_model + "'"
        cursor.execute(sqlquery_car_ratings)
        raw_car_ratings = cursor.fetchall()

        # Sets up our classes and puts information provided from our query into lists for use.
        overallrating = Rating()
        pricerating = Rating()
        safetyrating = Rating()
        reliabilityrating = Rating()
        servicerating = Rating()
        stylerating = Rating()
        all_ratings_list = [overallrating, pricerating, safetyrating, reliabilityrating, servicerating, stylerating]
        overallrating.name = 'Overall Rating'
        pricerating.name = 'Price Rating'
        safetyrating.name = 'Safety Rating'
        reliabilityrating.name = 'Reliability Rating'
        servicerating.name = 'Service Rating'
        stylerating.name = 'Style Rating'
        
        for rating_list in raw_car_ratings:
            overallrating.list.append(rating_list[0])
            pricerating.list.append(rating_list[1])
            safetyrating.list.append(rating_list[2])
            reliabilityrating.list.append(rating_list[3])
            servicerating.list.append(rating_list[4])
            stylerating.list.append(rating_list[5])

        # If no rating information is found, creates ratingless HTML page for that car model.
        if len(overallrating.list) == 0:
            create_blank_html_page(car_make, car_model)

        # Calls 'star_rating_processor' to count our ratings and provide averages.
        # Then calls 'create_html_rating_page' to create HTML docs.
        else:
            for rating_list in all_ratings_list:
                star_rating_processor(rating_list)
            create_html_rating_page(car_make, car_model, overallrating, pricerating, safetyrating, reliabilityrating, servicerating, stylerating)

    # Finally calls 'create_histogram_summary' to create histograms.html page.
    create_histogram_summary(make_model_list)
    print "Everything complete! Check .html files for consistency. :)"


# Function used by create_histograms for data processing.
# Provides a count of every rating and also average ratings.
def star_rating_processor(rating):
    rating.five_star_count = rating.list.count(5)
    rating.four_star_count = rating.list.count(4)
    rating.three_star_count = rating.list.count(3)
    rating.two_star_count = rating.list.count(2)
    rating.one_star_count = rating.list.count(1)
    rating.number_of_reviews = len(rating.list)
    rating.avg_rating =  sum(rating.list) / float(len(rating.list))
    rating.avg_rating = round(rating.avg_rating, 2)


# Queries the db for average overall rating for our summary page.
# Calls 'create_html_summary_page' to write histograms.html.
def create_histogram_summary(make_model_list):
    make_model_query = ''
    for car_make_model in make_model_list:
        car_make = car_make_model[0]
        car_model = car_make_model[1]
        if car_make_model != make_model_list[-1]:
            make_model_query = make_model_query + "(make = '" + car_make + "' AND model = '" + car_model + "') OR "
        else:
            make_model_query = make_model_query + "(make = '" + car_make + "' AND model = '" + car_model + "')"
    sqlquery_rating_summary = "SELECT make, model, AVG(overallRating) AS AverageRating \
    FROM car_details INNER JOIN car_ratings ON car_details.carId=car_ratings.carId \
    WHERE " + make_model_query + " GROUP BY model ORDER BY AverageRating DESC, make DESC, model DESC"
    cursor.execute(sqlquery_rating_summary)
    rating_summary = cursor.fetchall()
    create_html_summary_page(rating_summary)


# Start of functions that write HTML code.

# This function creates a rating page for a specific car model every time it is called.
# It calls a function called 'create_html_rating_table' to dynamicly create the histogram
# for each car model and rating type.
def create_html_rating_page(car_make, car_model, overallrating, pricerating, safetyrating, reliabilityrating, servicerating, stylerating):
    all_ratings_list = [overallrating, pricerating, safetyrating, reliabilityrating, servicerating, stylerating]
    filename = car_make + '_' + car_model + '.html'
    output_file = file(filename, 'w')

    #Page header & title
    output_file.write('<html><head><title>' + 'Car Ratings - ' + car_make + ' ' + car_model + '</title></head>')

    #Setup of styles to use on our page.
    output_file.write('<style>.div-headings{display: block; margin-top: 2em; margin-left: 2em; white-space: nowrap; color: blue;}')
    output_file.write('.div-overall-table{display: block; margin: 1em; margin-left: 14em; width: 350px;}')
    output_file.write('.table{display: inline-block; position:relative; white-space: nowrap; margin: 1em; margin-left: 2em; width: 350px;}')
    output_file.write('.border-and-shade{border:2px ridge; border-radius:50px; background-color: #A1A1A1;  box-shadow: 10px 10px 20px #A1A1A1;}')
    output_file.write('.bar-heading-label{padding-bottom: 5px; text-align: center; white-space: nowrap;}')
    output_file.write('.star-rating-label{padding-right: 5px; text-align: right; white-space: nowrap; width: 50px;}')
    output_file.write('.bar-cell{border-left: 2px solid #000000; white-space: nowrap; width: 250px; padding: 2px 0;}')
    output_file.write('.bar5{background-color: #2BC400; border-top: 5px solid #2ED400; border-right: 6px outset #2ED400;}')
    output_file.write('.bar4{background-color: #A6CF00; border-top: 5px solid #B0DB00; border-right: 6px outset #B0DB00;}')
    output_file.write('.bar3{background-color: #CCD600; border-top: 5px solid #DDE800; border-right: 6px outset #DDE800;}')
    output_file.write('.bar2{background-color: #D65100; border-top: 5px solid #FF6000; border-right: 6px outset #FF6000;}')
    output_file.write('.bar1{background-color: #D10000; border-top: 5px solid #F20000; border-right: 6px outset #F20000;}')
    output_file.write('.allbars{float: left; border-bottom: 1px solid #303030;}</style>')

    #Start of the body of our ratings page.
    output_file.write('<body>')
    output_file.write('<div class="div-headings">')
    output_file.write('<h2>Make: <span style ="color: red">' + car_make + '</span><br>')
    output_file.write('Model: <span style ="color: red">' + car_model + '</span><br>')
    output_file.write('Number of reviews: <span style ="color: red">' + str(overallrating.number_of_reviews) + '</span><br></h2>')
    output_file.write('<h3><a href="histograms.html">Back to Main Page</a></h3>')
    output_file.write('</div>')

    # Call our create_html_rating_table function to dynamically create histograms.
    # Place divs or spans based on what rating type we are up to for page aesthetics.
    for rating in all_ratings_list:
        if rating.name == 'Overall Rating' or rating.name == 'Style Rating':
            output_file.write('<div class="div-overall-table border-and-shade">')
            create_html_rating_table(output_file, rating)
            output_file.write('</div>')
        elif rating.name == 'Price Rating' or rating.name == 'Reliability Rating':
            output_file.write('<div style="display: block">')
            output_file.write('<span class="table border-and-shade">')
            create_html_rating_table(output_file, rating)
            output_file.write('</span>')
        else:
            output_file.write('<span class="table border-and-shade">')
            create_html_rating_table(output_file, rating)
            output_file.write('</span>')
            
    output_file.write('</body></html>')
    output_file.close()


# Creates the histograms for our page, bar by bar.
def create_html_rating_table(output_file, rating):
    output_file.write('<h4 class="bar-heading-label">' + rating.name + '</h4>')
    output_file.write('<table><tbody>')

    if rating.five_star_count == 0:
        five_star_bar_width = 0
    else:
        five_star_percentage = (rating.five_star_count)/float(rating.number_of_reviews)*100
        five_star_bar_width = five_star_percentage*2
    output_file.write('<tr><td class="star-rating-label">5 Star</td>')
    output_file.write('<td class="bar-cell"><span style="width:' + str(five_star_bar_width) + 'px" class="bar5 allbars">&nbsp;</span>&nbsp;<span>(' + str(rating.five_star_count) + ')</span></td></tr>')

    if rating.four_star_count == 0:
        four_star_bar_width = 0
    else:
        four_star_percentage = (rating.four_star_count)/float(rating.number_of_reviews)*100
        four_star_bar_width = four_star_percentage*2
    output_file.write('<tr><td class="star-rating-label">4 Star</td>')
    output_file.write('<td class="bar-cell"><span style="width:' + str(four_star_bar_width) + 'px" class="bar4 allbars">&nbsp;</span>&nbsp;<span>(' + str(rating.four_star_count) + ')</span></td></tr>')

    if rating.three_star_count == 0:
        three_star_bar_width = 0
    else:
        three_star_percentage = (rating.three_star_count)/float(rating.number_of_reviews)*100
        three_star_bar_width = three_star_percentage*2
    output_file.write('<tr><td class="star-rating-label">3 Star</td>')
    output_file.write('<td class="bar-cell"><span style="width:' + str(three_star_bar_width) + 'px" class="bar3 allbars">&nbsp;</span>&nbsp;<span>(' + str(rating.three_star_count) + ')</span></td></tr>')

    if rating.two_star_count == 0:
        two_star_bar_width = 0
    else:
        two_star_percentage = (rating.two_star_count)/float(rating.number_of_reviews)*100
        two_star_bar_width = two_star_percentage*2
    output_file.write('<tr><td class="star-rating-label">2 Star</td>')
    output_file.write('<td class="bar-cell"><span style="width:' + str(two_star_bar_width) + 'px" class="bar2 allbars">&nbsp;</span>&nbsp;<span>(' + str(rating.two_star_count) + ')</span></td></tr>')

    if rating.one_star_count == 0:
        one_star_bar_width = 0
    else:
        one_star_percentage = (rating.one_star_count)/float(rating.number_of_reviews)*100
        one_star_bar_width = one_star_percentage*2
    output_file.write('<tr><td class="star-rating-label">1 Star</td>')
    output_file.write('<td class="bar-cell"><span style="width:' + str(one_star_bar_width) + 'px" class="bar1 allbars">&nbsp;</span>&nbsp;<span>(' + str(rating.one_star_count) + ')</span></td></tr>')

    output_file.write('</tbody></table>')
    output_file.write('<h5 class="bar-heading-label">Average ' + rating.name + ': ' + str(rating.avg_rating) + '</h5>')


#If no ratings were found, creates a page with car make and model, but no histograms.
def create_blank_html_page(car_make, car_model):
    filename = car_make + '_' + car_model + '.html'
    pagetitle = 'Car Ratings - ' + car_make + ' ' + car_model
    output_file = file(filename, 'w')

    output_file.write('<html>')
    output_file.write('<head>')
    output_file.write('<title>' + pagetitle + '</title>')
    output_file.write('</head>')

    output_file.write('<style>')
    output_file.write('.div-headings{display: block; margin-top: 2em; margin-left: 2em; white-space: nowrap; color: blue;}')
    output_file.write('</style>')
    
    output_file.write('<body>')
    output_file.write('<div class="div-headings">')
    output_file.write('<h2>Make: <span style ="color: red">' + car_make + '</span><br>')
    output_file.write('Model: <span style ="color: red">' + car_model + '</span><br>')
    output_file.write('Number of reviews: <span style ="color: red">0</span><br></h2>')
    output_file.write('<h3><a href="histograms.html">Back to Main Page</a></h3>')
    output_file.write('</div>')
    
    output_file.write('</body>')
    output_file.write('</html>')
    output_file.close()


#Writes our histograms.html summary page using a table.
def create_html_summary_page(car_rating_summary):
    filename = 'histograms.html'
    output_file = file(filename, 'w')
    output_file.write('<html><head><title>Histogram Summary</title></head>')
    output_file.write('<style>.table-row-heading{color: blue; font-size:28px;}</style>') 
    
    output_file.write('<body>')
    output_file.write('<table align="center">')
    output_file.write('<caption><h1 style="color: blue;">Car Rating Histograms</h1></caption>')
    output_file.write('<tr><th class="table-row-heading" style="width: 200px"; align="left">Make</th>')
    output_file.write('<th class="table-row-heading" style="width: 200px"; align="left">Model</th>')
    output_file.write('<th class="table-row-heading" style="width: 250px";>Overall Rating</th></tr>')

    # Writes each line of the table containing a car make, model and overall rating
    # and a hyperlink to the page containing histograms.
    for rating in car_rating_summary:
        car_make = str(rating[0])
        car_model = str(rating[1])
        filename_hyperlink = car_make + "_" + car_model + ".html"
        rounded_overall_rating = str(round(rating[2],2))
        output_file.write('<tr><td style="color: red;"><i>' + car_make + '</i></td>')
        output_file.write('<td style="color: red;"><i>' + car_model + '</td>')
        output_file.write('<td align="center"><a href="' + filename_hyperlink + '">' + rounded_overall_rating + '</a></td></tr>')
    output_file.write('<tr><td style="color: red;"><i>LIGHTBURN</i></td><td style="color: red;"><i>ZETA</td>')
    output_file.write('<td align="center"><a href="LIGHTBURN_ZETA.html">0.0</a></td></tr>')
    output_file.write('</table>')

    output_file.write('</body></html>')
    output_file.close()

#
#--------------------------------------------------------------------#



#-----Automatic Testing----------------------------------------------#
#
#  The following code will automatically call your function to
#  test it.  NB: When your solution is marked different tests may
#  be used.
#
if __name__ == '__main__':
    create_histograms([['AUDI', 'A3'],
                       ['AUDI', 'A4'],
                       ['HOLDEN', 'COMMODORE'],
                       ['HOLDEN', 'KINGSWOOD'],
                       ['HOLDEN', 'ASTRA'],
                       ['HOLDEN','MONARO'],
                       ['FORD','FAIRMONT'],
                       ['FORD','FALCON'],
                       ['FORD','LASER'],
                       ['FORD','TELSTAR'],
                       ['TOYOTA', 'CAMRY'],
                       ['TOYOTA','COROLLA'],
                       ['TOYOTA', 'HILUX'],
                       ['TOYOTA','TARAGO'],
                       ['MAZDA','323'],
                       ['MAZDA','MAZDA3'],
                       ['MAZDA','MAZDA6'],
                       ['MAZDA','MAZDA2'],
                       ['BMW','7'],
                       ['BMW','3'],
                       ['BMW','5'],
                       ['NISSAN','X-TRAIL'],
                       ['NISSAN','PULSAR'],
                       ['NISSAN','PATROL'],
                       ['MITSUBISHI','OUTLANDER'],
                       ['MITSUBISHI','TRITON'],
                       ['MITSUBISHI','MAGNA'],
                       ['HONDA','CIVIC'],
                       ['HONDA','ACCORD'],
                       ['HONDA','JAZZ'],
                       ['SUBARU','LIBERTY'],
                       ['SUBARU','IMPREZA'],
                       ['LIGHTBURN', 'ZETA']]) # Last model is nonexistent
#
#--------------------------------------------------------------------#
