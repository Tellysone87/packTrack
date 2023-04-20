--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Ubuntu 13.10-1.pgdg22.04+1)
-- Dumped by pg_dump version 13.10 (Ubuntu 13.10-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: tellysone
--

CREATE TABLE public.items (
    item_id integer NOT NULL,
    package_id integer NOT NULL,
    quantity integer,
    name character varying
);


ALTER TABLE public.items OWNER TO tellysone;

--
-- Name: items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: tellysone
--

CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.items_item_id_seq OWNER TO tellysone;

--
-- Name: items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tellysone
--

ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;


--
-- Name: packages; Type: TABLE; Schema: public; Owner: tellysone
--

CREATE TABLE public.packages (
    package_id integer NOT NULL,
    user_id integer NOT NULL,
    tracking_number character varying(100) NOT NULL,
    shipped_date timestamp without time zone,
    location character varying(100) NOT NULL,
    status character varying(100) NOT NULL,
    merchant character varying(100),
    carrier character varying(100)
);


ALTER TABLE public.packages OWNER TO tellysone;

--
-- Name: packages_package_id_seq; Type: SEQUENCE; Schema: public; Owner: tellysone
--

CREATE SEQUENCE public.packages_package_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.packages_package_id_seq OWNER TO tellysone;

--
-- Name: packages_package_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tellysone
--

ALTER SEQUENCE public.packages_package_id_seq OWNED BY public.packages.package_id;


--
-- Name: statuses; Type: TABLE; Schema: public; Owner: tellysone
--

CREATE TABLE public.statuses (
    status_id integer NOT NULL,
    package_id integer NOT NULL,
    status character varying(100),
    date timestamp without time zone
);


ALTER TABLE public.statuses OWNER TO tellysone;

--
-- Name: statuses_status_id_seq; Type: SEQUENCE; Schema: public; Owner: tellysone
--

CREATE SEQUENCE public.statuses_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statuses_status_id_seq OWNER TO tellysone;

--
-- Name: statuses_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tellysone
--

ALTER SEQUENCE public.statuses_status_id_seq OWNED BY public.statuses.status_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: tellysone
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fname character varying(25) NOT NULL,
    lname character varying(25) NOT NULL,
    address character varying(50) NOT NULL,
    city character varying(25) NOT NULL,
    state character varying(25) NOT NULL,
    zipcode integer NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(150) NOT NULL
);


ALTER TABLE public.users OWNER TO tellysone;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: tellysone
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO tellysone;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tellysone
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: items item_id; Type: DEFAULT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);


--
-- Name: packages package_id; Type: DEFAULT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.packages ALTER COLUMN package_id SET DEFAULT nextval('public.packages_package_id_seq'::regclass);


--
-- Name: statuses status_id; Type: DEFAULT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.statuses ALTER COLUMN status_id SET DEFAULT nextval('public.statuses_status_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: tellysone
--

COPY public.items (item_id, package_id, quantity, name) FROM stdin;
\.


--
-- Data for Name: packages; Type: TABLE DATA; Schema: public; Owner: tellysone
--

COPY public.packages (package_id, user_id, tracking_number, shipped_date, location, status, merchant, carrier) FROM stdin;
\.


--
-- Data for Name: statuses; Type: TABLE DATA; Schema: public; Owner: tellysone
--

COPY public.statuses (status_id, package_id, status, date) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tellysone
--

COPY public.users (user_id, fname, lname, address, city, state, zipcode, email, password) FROM stdin;
\.


--
-- Name: items_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tellysone
--

SELECT pg_catalog.setval('public.items_item_id_seq', 1, false);


--
-- Name: packages_package_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tellysone
--

SELECT pg_catalog.setval('public.packages_package_id_seq', 1, false);


--
-- Name: statuses_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tellysone
--

SELECT pg_catalog.setval('public.statuses_status_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tellysone
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);


--
-- Name: packages packages_pkey; Type: CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (package_id);


--
-- Name: statuses statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (status_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: items items_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(package_id);


--
-- Name: packages packages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: statuses statuses_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tellysone
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(package_id);


--
-- PostgreSQL database dump complete
--

