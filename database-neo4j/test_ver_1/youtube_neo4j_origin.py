from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
    def create_platform(self, platform):
        with self.driver.session() as session:
            session.write_transaction(self._create_platform, platform)
    @staticmethod
    def _create_platform(tx, platform):
        query = (
            "CREATE (p:Platform { name: $platform }) "
        )
        tx.run(query, platform=platform)
    def create_content(self, url, title, date, n_view, n_comment, good, warm, sad, angry, want, crawl_time):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_content, url, title, date, n_view, n_comment, good, warm, sad, angry, want, crawl_time
            )
            # for content in result:
            #     print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_content(tx, url, title, date, n_view, n_comment, good, warm, sad, angry, want, crawl_time):

        query = (
            "CREATE (c:Content { url: $url, title: $title, date: $date })"
            "CREATE (v:View { n: $n_view })"
            "CREATE (com:Comment { n: $n_comment })"
            "CREATE (react:Reaction { good: $good, warm: $warm, sad: $sad, angry: $angry, want: $want })"
            "CREATE (ct: CrawlTime { time: $crawl_time })"
            "CREATE (c)-[:COMMENTS]->(com)"
            "CREATE (c)-[:REACTS]->(react)"
            "CREATE (c)-[:VIEWS]->(v)"
            "CREATE (c)-[:CRAWLED_AT]->(ct)"
            "RETURN c, v, com, react, ct"
        )
        result = tx.run(query, url=url, title=title, date=date, n_view=n_view, n_comment=n_comment,\
            good=good, warm=warm, sad=sad, angry=angry, want=want, crawl_time=crawl_time)
        try:
            # 일부만 작성
            return [{"c": row["c"]["title"], "v": row["v"]["n"], "com": row["com"]["n"], \
                "react": row["react"], "ct": row["ct"]["time"]} for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_keyword(self, keyword, url):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_keyword, keyword)
            if len(result) == 0:
                result = session.write_transaction(self._create_keyword, keyword)
            session.write_transaction(self._match_content_and_keyword, url, keyword)
    @staticmethod
    def _match_content_and_keyword(tx, url, keyword):
        query = (
            "MATCH (c:Content) "
            "WHERE c.url = $url "
            "MATCH (k:Keyword) "
            "WHERE k.name = $keyword "
            "CREATE (c)-[:EXTRACTS]->(k) "
        )
        tx.run(query, url=url, keyword=keyword)
    @staticmethod
    def _create_keyword(tx, keyword):
        query = (
            "CREATE (k: Keyword { name: $keyword }) "
            "RETURN k "
            )
        #result = tx.run(query, keyword=keyword)
        result = tx.run(query, keyword=keyword)
    @staticmethod
    def _find_and_return_keyword(tx, keyword):
        query = (
            "MATCH (k:Keyword) "
            "WHERE k.name = $keyword "
            "RETURN k.name AS name "
        )
        result = tx.run(query, keyword=keyword)
        res = [row["name"] for row in result]
        if res == None:
            return None
        else:
            return res
    


    def create_creator(self, creator, url, platform):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_creator, creator)
            if len(result) == 0:
                session.write_transaction(self._create_creator, creator)
                session.write_transaction(self._match_creator_and_platform, creator, platform)
            session.write_transaction(self._match_content_and_creator, url, creator)
    @staticmethod
    def _match_content_and_creator(tx, url, creator):
        query = (
            "MATCH (c:Content) "
            "WHERE c.url = $url "
            "MATCH (cr:Creator) "
            "WHERE cr.name = $creator "
            "CREATE (cr)-[:MAKES]->(c) "
        )
        tx.run(query, url=url, creator=creator)
    @staticmethod
    def _create_creator(tx, creator):
        query = (
            "CREATE (c: Creator { name: $creator, type: 'press' }) "
            "RETURN c"
            )
        #result = tx.run(query, keyword=keyword)
        result = tx.run(query, creator=creator)
    @staticmethod
    def _match_creator_and_platform(tx, creator, platform):
        query = (
            "MATCH (p:Platform) "
            "WHERE p.name = $platform "
            "MATCH (cr:Creator) "
            "WHERE cr.name = $creator "
            "CREATE (cr)-[:USES]->(p) "
        )
        tx.run(query, platform=platform, creator=creator)
    @staticmethod
    def _find_and_return_creator(tx, creator):
        query = (
            "MATCH (c:Creator) "
            "WHERE c.name = $creator "
            "RETURN c.name AS name "
        )
        result = tx.run(query, creator=creator)
        res = [row["name"] for row in result]
        if res == None:
            return None
        else:
            return res
if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    bolt_url = "bolt://localhost:7687"
    user = "neo4j"
    password = "neo4j123"
    app = App(bolt_url, user, password)
    #create platform
    app.create_platform('Naver')
    #data part
    
    value={'crawl_time': '2021-04-27/22', 'category': 'age', 'age': '40대', 'sex': '남성', 'rank': 1, 'url': 'https://v.daum.net/v/20210427205708037', 'title': [['학생', 'OCCUPATION'], ['상담교사', 'CIVILIZATION']], 'press': 'SBS', 'date': '2021. 04. 27. 20:57', 'n_comment': 1625, 'n_reaction_recommend': 30, 'n_reaction_like': 7, 'n_reaction_impress': 8, 'n_reaction_angry': 3192, 'n_reaction_sad': 20, 'n_reactions': '3257'}
    all = [value, value, value]
    for value in all:
        app.create_creator(value['press'],value['url'],'Naver')
    #press part
        app.create_content(value['url'],"학생 상담교사",value['date'],value['n_reactions'],value['n_comment'],10,11,12,13,14,value['crawl_time'])
        for elem in value['title']:
            print(elem)
            app.create_keyword(elem[0],value['url'])
    app.close()
