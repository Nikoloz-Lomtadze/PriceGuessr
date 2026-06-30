import random
# ეს ალგორითმი მუშაობს ასე: ჩვენ ვალაგებთ გამოცნობილ კატეგორიებს პროცენტულობით, თუ გამოცნობილ კატეგორიებზე
# მონაცემები არ გვაქვს მაშინ რანდომად ვიღებთ, თუ ყველაზე გამოვნობილი კატეგორიის პროცენტულობა მეტია 33 ზე მაშინ
# ავიღებთ რანდომულად მის საწინააღმდეგოს თუ არა მაშინ, ვიღებთ ყველაზე ნაკლებათ გამოცნობილს. 
class CategoryAdapter: 
    def __init__(self,database):
        self.database = database
        self.known_categories = [ # კატეგორიები რომლებიც ვიცით (მაგალითად, ისე უფრო მეტია)
            "electronics",
            "fashion",
            "sports",
            "books",
            "home",
            "toys"
                                ]
        self.opposite_categories = { # საპირისპირო კატეგორიები 
            "electronics":["fashion","sports","books","home","toys"],
            "fashion":["electronics","sports","books","home","toys"],
            "sports":["fashion","electronics","books","home","toys"],
            "books":["electronics","sports","fashion","home","toys"],
            "home":["fashion","electronics","sports","books","toys"],
            "toys":["electronics","sports","fashion","home","books"],
                                   }
        self.category_words = { # თვითონ გარკვეულ კატეგორიაში შემავალი keyword-ები
            "electronics": ["phone", "keyboard", "camera", "computer", "headphone", "gaming"],
            "fashion": ["shirt", "shoes", "jacket", "clothing", "watch", "dress"],
            "sports": ["sport", "football", "basketball", "fitness", "running"],
            "books": ["book", "novel", "textbook", "manga"],
            "home": ["home", "kitchen", "furniture", "garden"],
            "toys": ["toy", "lego", "game", "puzzle"]
                              }
    def normalize_category(self, category_text): #კატეგორიის სახელის ნორმალიზება
        if category_text is None:
            return "unknown"
        category_text = category_text.lower()
        for category in self.category_words:
            for word in self.category_words[category]: #ამოწმებს თუ ჩვენი ტექსტი შედის რომელიმე ჩვენით შეზღუდულ კატეგორიებში
                if word in category_text:
                    return category
        return "unknown"
    


    def get_category_stats(self, user_id): # ვიღებთ ლისტს სადაც დალაგენბულია ყველაზე გამოცნობადი კატეგორიები
        conn = self.database.connect()
        cursor = conn.cursor()

        # ამ პრომპტით ჩვენ ვითვლით გარკეული კატეგორიის რამდენი გამოვიცანით რათა გავიგოთ რომლებს ვიცნობთ მეტად
        prompt = """ 
        SELECT
        game_rounds.category_guessed,
        COUNT(*) AS guess_count
        FROM game_rounds
        JOIN games ON games.id = game_rounds.game_id
        WHERE games.user_id = ?
        GROUP BY game_rounds.category_guessed
        ORDER BY guess_count DESC
        """
        cursor.execute(prompt, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        category_counts = {}
        for row in rows:
            category = self.normalize_category(row["category_guessed"]) #ნორმალიზირებული კატეგორია ჩვენი ლისტიდან (სულ ზემოთ)
            guess_count = row["guess_count"] # რამდენჯერ გამოვიცანით
            
            #თუ არა გვაქვს დიქშინერიშ ვქნმით შიგნით და ვამატებთ გამოცნობის რაოდენობას
            if category not in category_counts:
                category_counts[category] = 0

            category_counts[category] += guess_count

        total_guesses = sum(category_counts.values()) # სულ ყველა კატეგორია რამდენჯერ გამოვიცანით
        stats = []
        for category in category_counts:
            percent = category_counts[category] / total_guesses # გამოცნობის პროცენტულობა
            stats.append({ # ახლა ლისტში ვამატებთ ყველ კატეგორიას გამოცნობის რაოდენობასთან და პროცენტულობასთან ერთად
                "category": category,
                "guess_count": category_counts[category],
                "percent": percent
                         })

        stats.sort(key=lambda item: item["guess_count"], reverse=True) ###
        #ეს ეხლა ვისწავლე, lambda item-ის მიხედვით ალაგებს რევერსულად ჩვენ ლისტს

        return stats

    def get_next_category(self, user_id): 
        stats = self.get_category_stats(user_id) # დალაგებული ლისტი კატეგორიებით პროცენტულობით და რაოდენობით

        if len(stats) == 0: # იმ შემთხვევაში თუ ჯერ არაფერი არ გამოგვიცნია რანდომად ავიღოთ კატეგორია
            return random.choice(self.known_categories)
        most_guessed = stats[0] # ყველაზე გამოცნობილი აითემი არის პირველი

        if most_guessed["percent"] >= 0.33: # ზედმეტად მეტად გამოცნობილია ეს კატეგორია თუ არა
            category = most_guessed["category"]
            if category in self.opposite_categories:
                return random.choice(self.opposite_categories[category]) # თუ ასეა მაშინ ვიღებთ საწინააღმდეგო კატეგორიებიდან ერთ-ერთს
        guessed_categories = []

        for item in stats:
            guessed_categories.append(item["category"])
        least_used_categories = []

        for category in self.known_categories:
            if category not in guessed_categories:
                least_used_categories.append(category)

        if len(least_used_categories) > 0:
            return random.choice(least_used_categories)

        least_guessed = stats[-1]
        return least_guessed["category"]