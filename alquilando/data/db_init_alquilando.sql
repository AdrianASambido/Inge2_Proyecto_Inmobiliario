--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-05-26 16:03:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4890 (class 1262 OID 16546)
-- Name: db_init_alquilando; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE db_init_alquilando WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Argentina.1252';


ALTER DATABASE db_init_alquilando OWNER TO postgres;

\connect db_init_alquilando

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 16548)
-- Name: administrador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administrador (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    apellido character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.administrador OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16547)
-- Name: administrador_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.administrador_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.administrador_id_seq OWNER TO postgres;

--
-- TOC entry 4891 (class 0 OID 0)
-- Dependencies: 217
-- Name: administrador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administrador_id_seq OWNED BY public.administrador.id;


--
-- TOC entry 220 (class 1259 OID 16557)
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    apellido character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    dni character varying(20),
    telefono character varying(20),
    numero_tarjeta character varying(30),
    nacionalidad character varying(20)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16556)
-- Name: cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_id_seq OWNER TO postgres;

--
-- TOC entry 4892 (class 0 OID 0)
-- Dependencies: 219
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- TOC entry 222 (class 1259 OID 16566)
-- Name: encargado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.encargado (
    id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    apellido character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.encargado OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16565)
-- Name: encargado_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.encargado_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.encargado_id_seq OWNER TO postgres;

--
-- TOC entry 4893 (class 0 OID 0)
-- Dependencies: 221
-- Name: encargado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.encargado_id_seq OWNED BY public.encargado.id;


--
-- TOC entry 232 (class 1259 OID 16661)
-- Name: imagen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.imagen (
    id integer NOT NULL,
    url text NOT NULL,
    titulo character varying(100),
    descripcion text,
    es_principal boolean DEFAULT false,
    fecha_subida timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    propiedad_id integer NOT NULL
);


ALTER TABLE public.imagen OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16660)
-- Name: imagen_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.imagen_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.imagen_id_seq OWNER TO postgres;

--
-- TOC entry 4894 (class 0 OID 0)
-- Dependencies: 231
-- Name: imagen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.imagen_id_seq OWNED BY public.imagen.id;


--
-- TOC entry 230 (class 1259 OID 16622)
-- Name: opinion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opinion (
    id integer NOT NULL,
    comentario text,
    cantidad_estrellas integer NOT NULL,
    cliente_id integer NOT NULL,
    propiedad_id integer NOT NULL,
    CONSTRAINT opinion_cantidad_estrellas_check CHECK (((cantidad_estrellas >= 1) AND (cantidad_estrellas <= 5)))
);


ALTER TABLE public.opinion OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16621)
-- Name: opinion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opinion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.opinion_id_seq OWNER TO postgres;

--
-- TOC entry 4895 (class 0 OID 0)
-- Dependencies: 229
-- Name: opinion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opinion_id_seq OWNED BY public.opinion.id;


--
-- TOC entry 228 (class 1259 OID 16608)
-- Name: pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pago (
    id integer NOT NULL,
    reserva_id integer NOT NULL,
    monto numeric(10,2) NOT NULL,
    completado boolean DEFAULT false,
    CONSTRAINT pago_monto_check CHECK ((monto > (0)::numeric))
);


ALTER TABLE public.pago OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16607)
-- Name: pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pago_id_seq OWNER TO postgres;

--
-- TOC entry 4896 (class 0 OID 0)
-- Dependencies: 227
-- Name: pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pago_id_seq OWNED BY public.pago.id;


--
-- TOC entry 224 (class 1259 OID 16575)
-- Name: propiedad; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.propiedad (
    id integer NOT NULL,
    dpto character varying(20),
    piso character varying(10),
    numero character varying(10),
    calle character varying(100),
    cantidad_ambientes integer,
    petfriendly boolean DEFAULT false,
    listada boolean DEFAULT true,
    encargado_id integer,
    pais character varying(40),
    provincia character varying(40),
    ciudad character varying(40),
    valor_por_noche numeric(10,2),
    alquilada boolean DEFAULT false,
    publicada boolean DEFAULT true,
    codigo_postal character varying(20),
    CONSTRAINT propiedad_cantidad_ambientes_check CHECK ((cantidad_ambientes >= 1))
);


ALTER TABLE public.propiedad OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16574)
-- Name: propiedad_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.propiedad_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.propiedad_id_seq OWNER TO postgres;

--
-- TOC entry 4897 (class 0 OID 0)
-- Dependencies: 223
-- Name: propiedad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.propiedad_id_seq OWNED BY public.propiedad.id;


--
-- TOC entry 226 (class 1259 OID 16590)
-- Name: reserva; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reserva (
    id integer NOT NULL,
    fecha_in date NOT NULL,
    fecha_out date NOT NULL,
    cliente_id integer NOT NULL,
    propiedad_id integer NOT NULL,
    CONSTRAINT fechas_validas CHECK ((fecha_in < fecha_out))
);


ALTER TABLE public.reserva OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16589)
-- Name: reserva_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reserva_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reserva_id_seq OWNER TO postgres;

--
-- TOC entry 4898 (class 0 OID 0)
-- Dependencies: 225
-- Name: reserva_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;


--
-- TOC entry 4676 (class 2604 OID 16551)
-- Name: administrador id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador ALTER COLUMN id SET DEFAULT nextval('public.administrador_id_seq'::regclass);


--
-- TOC entry 4677 (class 2604 OID 16560)
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- TOC entry 4678 (class 2604 OID 16569)
-- Name: encargado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado ALTER COLUMN id SET DEFAULT nextval('public.encargado_id_seq'::regclass);


--
-- TOC entry 4688 (class 2604 OID 16664)
-- Name: imagen id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen ALTER COLUMN id SET DEFAULT nextval('public.imagen_id_seq'::regclass);


--
-- TOC entry 4687 (class 2604 OID 16625)
-- Name: opinion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion ALTER COLUMN id SET DEFAULT nextval('public.opinion_id_seq'::regclass);


--
-- TOC entry 4685 (class 2604 OID 16611)
-- Name: pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago ALTER COLUMN id SET DEFAULT nextval('public.pago_id_seq'::regclass);


--
-- TOC entry 4679 (class 2604 OID 16578)
-- Name: propiedad id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad ALTER COLUMN id SET DEFAULT nextval('public.propiedad_id_seq'::regclass);


--
-- TOC entry 4684 (class 2604 OID 16593)
-- Name: reserva id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);


--
-- TOC entry 4870 (class 0 OID 16548)
-- Dependencies: 218
-- Data for Name: administrador; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrador (id, nombre, apellido, email, password) FROM stdin;
1	Lucía	Gómez	lucia@admin.com	admin123
2	Carlos	Pérez	carlos@admin.com	admin456
\.


--
-- TOC entry 4872 (class 0 OID 16557)
-- Dependencies: 220
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (id, nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad) FROM stdin;
1	María	López	maria@cliente.com	clave1	\N	\N	\N	\N
2	Juan	Martínez	juan@cliente.com	clave2	\N	\N	\N	\N
3	Adrian alejandro	Sambido	adriinform2021@gmail.com	clave3	\N	\N	\N	\N
4	Francisco	Rousseau	francisco@cliente.com	clave4	\N	\N	\N	\N
\.


--
-- TOC entry 4874 (class 0 OID 16566)
-- Dependencies: 222
-- Data for Name: encargado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.encargado (id, nombre, apellido, email, password) FROM stdin;
1	Ana	Ramírez	ana@encargado.com	enc123
2	Pedro	Sosa	pedro@encargado.com	enc456
\.


--
-- TOC entry 4884 (class 0 OID 16661)
-- Dependencies: 232
-- Data for Name: imagen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.imagen (id, url, titulo, descripcion, es_principal, fecha_subida, propiedad_id) FROM stdin;
\.


--
-- TOC entry 4882 (class 0 OID 16622)
-- Dependencies: 230
-- Data for Name: opinion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opinion (id, comentario, cantidad_estrellas, cliente_id, propiedad_id) FROM stdin;
1	Muy linda propiedad, todo limpio.	5	1	1
2	Buena ubicación pero algo ruidosa.	3	2	2
\.


--
-- TOC entry 4880 (class 0 OID 16608)
-- Dependencies: 228
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pago (id, reserva_id, monto, completado) FROM stdin;
1	1	50000.00	t
2	2	45000.00	f
\.


--
-- TOC entry 4876 (class 0 OID 16575)
-- Dependencies: 224
-- Data for Name: propiedad; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.propiedad (id, dpto, piso, numero, calle, cantidad_ambientes, petfriendly, listada, encargado_id, pais, provincia, ciudad, valor_por_noche, alquilada, publicada, codigo_postal) FROM stdin;
1	A	3	101	Calle Falsa	2	t	t	1	\N	\N	\N	\N	f	t	\N
2	B	1	202	Av. Siempre Viva	3	f	t	2	\N	\N	\N	\N	f	t	\N
\.


--
-- TOC entry 4878 (class 0 OID 16590)
-- Dependencies: 226
-- Data for Name: reserva; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reserva (id, fecha_in, fecha_out, cliente_id, propiedad_id) FROM stdin;
1	2025-06-01	2025-06-07	1	1
2	2025-07-10	2025-07-15	2	2
\.


--
-- TOC entry 4899 (class 0 OID 0)
-- Dependencies: 217
-- Name: administrador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administrador_id_seq', 1, false);


--
-- TOC entry 4900 (class 0 OID 0)
-- Dependencies: 219
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_seq', 4, true);


--
-- TOC entry 4901 (class 0 OID 0)
-- Dependencies: 221
-- Name: encargado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.encargado_id_seq', 1, false);


--
-- TOC entry 4902 (class 0 OID 0)
-- Dependencies: 231
-- Name: imagen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.imagen_id_seq', 1, false);


--
-- TOC entry 4903 (class 0 OID 0)
-- Dependencies: 229
-- Name: opinion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opinion_id_seq', 1, false);


--
-- TOC entry 4904 (class 0 OID 0)
-- Dependencies: 227
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pago_id_seq', 1, false);


--
-- TOC entry 4905 (class 0 OID 0)
-- Dependencies: 223
-- Name: propiedad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.propiedad_id_seq', 1, false);


--
-- TOC entry 4906 (class 0 OID 0)
-- Dependencies: 225
-- Name: reserva_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reserva_id_seq', 1, false);


--
-- TOC entry 4696 (class 2606 OID 16555)
-- Name: administrador administrador_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_email_key UNIQUE (email);


--
-- TOC entry 4698 (class 2606 OID 16553)
-- Name: administrador administrador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (id);


--
-- TOC entry 4700 (class 2606 OID 16564)
-- Name: cliente cliente_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_email_key UNIQUE (email);


--
-- TOC entry 4702 (class 2606 OID 16562)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- TOC entry 4704 (class 2606 OID 16573)
-- Name: encargado encargado_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_email_key UNIQUE (email);


--
-- TOC entry 4706 (class 2606 OID 16571)
-- Name: encargado encargado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_pkey PRIMARY KEY (id);


--
-- TOC entry 4716 (class 2606 OID 16670)
-- Name: imagen imagen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 16630)
-- Name: opinion opinion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_pkey PRIMARY KEY (id);


--
-- TOC entry 4712 (class 2606 OID 16615)
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id);


--
-- TOC entry 4708 (class 2606 OID 16583)
-- Name: propiedad propiedad_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_pkey PRIMARY KEY (id);


--
-- TOC entry 4710 (class 2606 OID 16596)
-- Name: reserva reserva_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id);


--
-- TOC entry 4723 (class 2606 OID 16671)
-- Name: imagen imagen_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id) ON DELETE CASCADE;


--
-- TOC entry 4721 (class 2606 OID 16631)
-- Name: opinion opinion_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id);


--
-- TOC entry 4722 (class 2606 OID 16636)
-- Name: opinion opinion_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);


--
-- TOC entry 4720 (class 2606 OID 16616)
-- Name: pago pago_reserva_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_reserva_id_fkey FOREIGN KEY (reserva_id) REFERENCES public.reserva(id) ON DELETE CASCADE;


--
-- TOC entry 4717 (class 2606 OID 16584)
-- Name: propiedad propiedad_encargado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_encargado_id_fkey FOREIGN KEY (encargado_id) REFERENCES public.encargado(id);


--
-- TOC entry 4718 (class 2606 OID 16597)
-- Name: reserva reserva_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id);


--
-- TOC entry 4719 (class 2606 OID 16602)
-- Name: reserva reserva_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);


-- Completed on 2025-05-26 16:03:26

--
-- PostgreSQL database dump complete
--

