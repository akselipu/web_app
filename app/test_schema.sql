INSERT INTO categories (name) VALUES ('Autot');
INSERT INTO categories (name) VALUES ('Lifestyle');
INSERT INTO categories (name) VALUES ('Matkustelu');
INSERT INTO categories (name) VALUES ('Eläimet');
INSERT INTO categories (name) VALUES ('Ruoka ja juoma');

insert into users (name, password) values ('jari', 'scrypt:32768:8:1$BUltrl6SG5HtHgr0$7b68b698c11c64ed19228eced8cafc4d437c04ae9dd85ded673555acee228e7f9442b7271bea33c095efe36fd505ee8f934b7c0979c0a443379f9484448b1b3c');
insert into users (name, password) values ('tiina', 'scrypt:32768:8:1$BUltrl6SG5HtHgr0$7b68b698c11c64ed19228eced8cafc4d437c04ae9dd85ded673555acee228e7f9442b7271bea33c095efe36fd505ee8f934b7c0979c0a443379f9484448b1b3c');
insert into users (name, password) values ('kalle', 'scrypt:32768:8:1$BUltrl6SG5HtHgr0$7b68b698c11c64ed19228eced8cafc4d437c04ae9dd85ded673555acee228e7f9442b7271bea33c095efe36fd505ee8f934b7c0979c0a443379f9484448b1b3c');
insert into users (name, password) values ('bloggaripro', 'scrypt:32768:8:1$BUltrl6SG5HtHgr0$7b68b698c11c64ed19228eced8cafc4d437c04ae9dd85ded673555acee228e7f9442b7271bea33c095efe36fd505ee8f934b7c0979c0a443379f9484448b1b3c');
insert into users (name, password) values ('Jykke', 'scrypt:32768:8:1$BUltrl6SG5HtHgr0$7b68b698c11c64ed19228eced8cafc4d437c04ae9dd85ded673555acee228e7f9442b7271bea33c095efe36fd505ee8f934b7c0979c0a443379f9484448b1b3c');

CREATE ROLE jari LOGIN PASSWORD 'h'; 
GRANT DELETE ON ALL TABLES IN SCHEMA public TO jari;
CREATE ROLE tiina LOGIN PASSWORD 'h'; 
GRANT DELETE ON ALL TABLES IN SCHEMA public TO tiina;
CREATE ROLE kalle LOGIN PASSWORD 'h'; 
GRANT DELETE ON ALL TABLES IN SCHEMA public TO kalle;
CREATE ROLE bloggaripro LOGIN PASSWORD 'h'; 
GRANT DELETE ON ALL TABLES IN SCHEMA public TO bloggaripro;
CREATE ROLE Jykke LOGIN PASSWORD 'h'; 
GRANT DELETE ON ALL TABLES IN SCHEMA public TO Jykke;

INSERT INTO posts (title, content, category_id, author_id) VALUES ('Mersu on paras', 'Uskomaton auto ajaa, suosittelen', 1, 1);
INSERT INTO posts (title, content, category_id, author_id) VALUES ('datsun', 'kova peli. Lorem ipsum on 1500-luvulta lähtien olemassa ollut teksti, jota käytetään usein täytetekstinä ulkoasun testaamiseen graafisessa suunnittelussa, kun oikeata tekstisisältöä ei vielä ole. Lorem ipsumia käytetään näyttämään, miltä esimerkiksi kirjasin tai julkaisun tekstin asettelu näyttävät. Jos julkaisun mallissa käytetään todellista kieltä, ihmiset yleensä keskittyvät tekstin sisältöön. Kun tekstiksi valitaan lorem ipsum, suunnittelijat ja julkaisijat saavat tarkastelijat keskittymään ulkoasuun sisällön sijasta. Lorem ipsum muistuttaa klassista latinaa. Se on muodostettu latinankielisestä tekstistä jättämällä pois sanoja ja niiden osia eikä siten varsinaisesti tarkoita mitään. Lorem ipsumista on useita erilaisia variaatioita. Tyypillisesti lorem ipsum näyttää seuraavalta: Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non provident, sunt in culpa qui official deserunt mollit anim id est laborum. Teksti on peräisin Ciceron teoksesta De finibus bonorum et malorum, jossa alkuperäinen teksti alkaa ”Neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit”, mikä tarkoittaa suunnilleen: ”Eikä ole ketään, joka pitää tuskasta sen itsensä tähden, ja sitä näin ollen haluaisi”.', 1, 2);
INSERT INTO posts (title, content, category_id, author_id) VALUES ('Kreikan loma', 'Oli ihana loma Kreikassa, ruoka oli hyvää ja juoma. Maisemat mahtavia!', 3, 3);
INSERT INTO posts (title, content, category_id, author_id) VALUES ('Oikeaoppinen avokadopasta', 'Avokapasta on hyvää! Muista lisätä parmesan ja pinjansiemenet, jotta saat täydellisen makuista pastaa.', 5, 4);
INSERT INTO posts (title, content, category_id, author_id) VALUES ('Lores for people', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 2, 5);

INSERT INTO comments (content, post_id, author_id) VALUES ('Ei kyl bemari on parempi', 1, 3);
INSERT INTO comments (content, post_id, author_id) VALUES ('Datsuni voittoon!!', 1, 2);
INSERT INTO comments (content, post_id, author_id) VALUES ('En kestä, niin ihanaa!', 3, 5);
INSERT INTO comments (content, post_id, author_id) VALUES ('Notta nyt!', 3, 4);
INSERT INTO comments (content, post_id, author_id) VALUES ('Onko noin?', 1, 2);
INSERT INTO comments (content, post_id, author_id) VALUES ('Kyllä!', 1, 1);