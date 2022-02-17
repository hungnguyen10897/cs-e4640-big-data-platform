DROP KEYSPACE IF EXISTS mysimpbdp;

CREATE KEYSPACE mysimpbdp WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

USE mysimpbdp;

CREATE TABLE reviews (
  marketplace TEXT,
  customer_id TEXT,
  review_id TEXT,
  product_id TEXT,
  product_parent TEXT,
  product_title TEXT,
  product_category TEXT,
  star_rating INT,
  helpful_votes INT,
  total_votes INT,
  vine TEXT,
  verified_purchase TEXT,
  review_headline TEXT,
  review_body TEXT,
  review_date TEXT,
  PRIMARY KEY (product_id, marketplace)
);

INSERT INTO reviews 
  (marketplace, customer_id, review_id, product_id, product_parent, product_title, product_category, star_rating, helpful_votes, total_votes, vine, verified_purchase, review_headline, review_body, review_date)
VALUES 
  ('US','24371595', 'R27ZP1F1CD0C3Y', 'B004LLIL5A', '346014806', 'Amazon eGift Card - Celebrate',	'Gift Card', 5, 0, 0, 'N', 'Y', 'Five Stars', 'Great birthday gift for a young adult.', '31.8.2015');

