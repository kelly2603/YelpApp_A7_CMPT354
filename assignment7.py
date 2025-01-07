import pymssql


def main():
    conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_htk', password='t2jYA77aY244HMFN', database='htk354')

    cursor = conn.cursor(as_dict=True)

    global uid
    uid = None

    ## Log in
    def log_in():
        global uid 
        print('Logging in... Please enter your user id:')
        uid = input().strip()

        cursor.execute(
            'SELECT * \
            FROM dbo.user_yelp \
            WHERE user_id = %s', uid
        )

        result = cursor.fetchone()

        if result:
            print("Log in successful!\n")
            main_menu()
        else:
            print("Log in unsuccessful. username doesn't exist in database. Please try again.")
            log_in()

    ## Business Review
    def bus_review():
        global uid
        import uuid
        import base64

        print("||REVIEW BUSINESS||")
        print("Enter the ID of the business you want to review:")
        bid = input()

        cursor.execute("SELECT stars, review_count, name FROM business WHERE business_id = %s",bid)

        result = cursor.fetchone()

        if result:
            # generate review ID
            generated_uuid = uuid.uuid4()
            uuid_bytes = generated_uuid.bytes
            base64_uuid = base64.urlsafe_b64encode(uuid_bytes).rstrip(b'=')
            reviewID = base64_uuid.decode('utf-8')

            currentStars = result['stars']
            currentRevCount = result['review_count']
            currentStars = float(currentStars)
            currentRevCount = int(currentRevCount)


            print(f"Reviewing business with id {bid}, current star {currentStars}, current review count {currentRevCount}")
            print("Enter the number of star for review (between 1 and 5):")
        
            star = int(input())

            

            # check if user already reviewed
            cursor.execute("SELECT review_id, stars FROM review WHERE business_id = %s AND user_id = %s", (bid, uid))
            r1 = cursor.fetchone()

            if r1 is not None:
                print("NOTE: since you have reviewed this business before, only your latest review will count towards the business' stars and review count")
                oldStar = r1["stars"]
                newStars = (currentStars * currentRevCount + star - oldStar)/(currentRevCount)
            else:
                currentRevCount += 1
                newStars = (currentStars * (currentRevCount-1) + star)/(currentRevCount)
            
            # insert new review into review table
            cursor.execute("""
            INSERT INTO review (review_id, user_id, business_id, stars, useful, funny, cool, date)
            VALUES (%s,%s,%s,%s,0,0,0,GETDATE());""", (reviewID, uid, bid, star))

            # update business stars
            cursor.execute("""
                UPDATE business
                SET stars = %s
                WHERE business_id = %s""", (newStars, bid))
            
            conn.commit()
        
            print(f"Updated business with id: {bid}, with new stars: {newStars:.1f}, and new review count: {currentRevCount}.\n")
        else:
            print(f"No business with id {bid} found\n")
        
        print("Enter '1' to return to main menu or '2' to review another business")
        uinput = input()

        if uinput == "1":
            main_menu()
        elif uinput == "2":
            bus_review()


    ## Search business
    def bus_search():
        print("\n||BUSINESS SEARCH||")
        print("Enter filters for search: \nName (or part of name):")
        name = input()
        print("City:")
        city = input()
        print("Minimum number of stars:")
        minStar = input()

        print("Select ordering options: 1.name, 2.city, 3.stars")
        print("Enter 1, 2 or 3 (Enter anything else for no ordering):")
        orderby = input()
        
        query = 'SELECT * FROM dbo.business WHERE 1=1'
        params = []

        if minStar:
            query += "AND stars >= %s"
            params.append(minStar)


        if city:
            query += "AND LOWER(city) = LOWER(%s)"
            params.append(city)

        if name:
            query += "AND LOWER(name) LIKE LOWER(%s)"
            params.append(f"%{name}%")
        

        if orderby == '1':
            query += "ORDER BY name ASC"
        elif orderby == '2':
            query += "ORDER BY city ASC"
        elif orderby == '3':
            query += "ORDER BY stars DESC"
        
        cursor.execute(query, tuple(params))

        results = cursor.fetchone()
        i = 1

        if results is not None:
            print("\nSEARCH RESULTS:")
            print("Bussiness(es) found with specified filter:")
            while results is not None:
                # Print attributes name, city, stars for each business
                print(f"{i}. ID: {results['business_id']}, Name: {results['name']}, Address: {results['address']}, City: {results['city']}, Stars: {results['stars']}.")

                results = cursor.fetchone()
                i += 1

            print("Enter '1' to return to main menu or '2' to review a business")
            uinput = input()
            if uinput == "1":
                main_menu()
            elif uinput == "2":
                bus_review()
        else:
            print("No business found with specified filter\n")
            print("Enter '1' to return to main menu or '2' to modify filters")
            uinput = input()
            if uinput == "1":
                main_menu()
            elif uinput == "2":
                bus_search()


    ## Friend user
    def u_friend():
        global uid
        print("||MAKE FRIEND||")
        print("Enter the ID of the user you want to make friend")
        fid = input()

        cursor.execute("SELECT user_id, name FROM user_yelp WHERE user_id = %s",fid)

        result = cursor.fetchone()

        if result:
            cursor.execute("SELECT * FROM friendship WHERE user_id = %s AND friend = %s", (uid,fid))
            r1 = cursor.fetchone()
            if r1:
                print("You are already friends with this user")
            else:
                cursor.execute("""
                INSERT INTO friendship (user_id, friend)
                VALUES (%s,%s);""", (uid, fid))
                print(f"Friendhsip added with user {fid}.")
            
            conn.commit()
        else:
            print(f"No user with id {fid} found\n")
        
        print("Enter '1' to return to main menu or '2' to add another friend")
        uinput = input()

        if uinput == "1":
            main_menu()
        elif uinput == "2":
            u_friend()


    ## User Search
    def u_search():
        print("\n||USER SEARCH||")
        print("Enter filters for search: \nName (or part of name):")
        name = input()
        print("Minimum Review Count:")
        minRevCount = input()
        print("Minimum Average Stars:")
        minAvgStar = input()
        
        query = 'SELECT * FROM dbo.user_yelp WHERE 1=1'
        params = []

        if name:
            query += "AND LOWER(name) LIKE LOWER(%s)"
            params.append(f"%{name}%")

        if minRevCount:
            query += "AND review_count >= %s"
            params.append(minRevCount)

        if minAvgStar:
            query += "AND average_stars >= %s"
            params.append(minAvgStar)

        query += "ORDER BY name ASC"
        
        cursor.execute(query, tuple(params))

        results = cursor.fetchone()
        i = 1

        if results is not None:
            print("\nSEARCH RESULTS:")
            print("User(s) found with specified filter:")
            while results is not None:
                # Print attributes name, city, stars for each business
                print(f"{i}. ID: {results['user_id']}, Name: {results['name']}, Review Count: {results['review_count']}, Useful: {results['useful']}, Funny: {results['funny']}, Cool: {results['cool']}, Average Stars: {results['average_stars']}, Yelping since: {results['yelping_since']}.")

                results = cursor.fetchone()
                i += 1

            print("\nEnter '1' to return to main menu or '2' to add a friend")
            uinput = input()
            if uinput == "1":
                main_menu()
            elif uinput == "2":
                u_friend()
        else:
            print("No users found with specified filter\n")
            print("Enter '1' to return to main menu or '2' to modify filters")
            uinput = input()
            if uinput == "1":
                main_menu()
            elif uinput == "2":
                u_search()
    

    # Main Menu
    def main_menu():
        print("||MAIN MENU||")
        print("Pick an option to proceed:\n1. Search Business\n2. Search User\nEnter 1 or 2:")
        uinput = input()

        if uinput == '1':
            bus_search()
        elif uinput == '2':
            u_search()
 
    

    ## start application
    print("~~WELCOME TO YELP APPLICATION~~")
    log_in()


    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()