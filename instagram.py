from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


class Instagram:
    def get_from_json(self):
        ...
    def get_from_html(self, html_file):
        users_dict = defaultdict(str)
        soup = BeautifulSoup(html_file.read(), "html.parser")
        main_divs = soup.find("div", attrs={"role": "main"})
        if main_divs:
            for link in main_divs.find_all("a"):
                users_dict[link.text] = link["href"]
        return users_dict
    
    def get_users_from_file(self, file: UploadedFile):
        if file.name.endswith(".html"):
            users = self.get_from_html(file)
        elif file.name.endswith(".json"):
            users = self.get_from_json(file)
        else:
            raise NotImplemented
        return users
    def get_users_df(self, user_object: dict) -> pd.DataFrame:
        df = pd.DataFrame(list(user_object.items()), columns=["Name", "Link"])
        df["Link"] = df["Link"].apply(
            lambda x: f'<a href="{x}" target="_blank">Click Here</a>'
        )
        return df
    
    def master(self, followers_file: UploadedFile, following_file: UploadedFile) -> pd.DataFrame:
        followers = self.get_users_from_file(followers_file)
        followings = self.get_users_from_file(following_file)
        followers_user = followers.keys()
        not_following_users = {}
        for following in followings.keys():
            if following not in followers_user:
                not_following_users[following] = followings[following]
        
        return self.get_users_df(not_following_users)



        
