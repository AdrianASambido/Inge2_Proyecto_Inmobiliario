--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-18 13:04:47

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
-- TOC entry 218 (class 1259 OID 24871)
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
-- TOC entry 217 (class 1259 OID 24870)
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
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 217
-- Name: administrador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administrador_id_seq OWNED BY public.administrador.id;


--
-- TOC entry 220 (class 1259 OID 24880)
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
    nacionalidad character varying(50)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24879)
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
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 219
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- TOC entry 222 (class 1259 OID 24889)
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
-- TOC entry 221 (class 1259 OID 24888)
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
-- TOC entry 4991 (class 0 OID 0)
-- Dependencies: 221
-- Name: encargado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.encargado_id_seq OWNED BY public.encargado.id;


--
-- TOC entry 232 (class 1259 OID 24965)
-- Name: imagen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.imagen (
    id integer NOT NULL,
    url text NOT NULL,
    propiedad_id integer NOT NULL
);


ALTER TABLE public.imagen OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 24964)
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
-- TOC entry 4992 (class 0 OID 0)
-- Dependencies: 231
-- Name: imagen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.imagen_id_seq OWNED BY public.imagen.id;


--
-- TOC entry 230 (class 1259 OID 24945)
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
-- TOC entry 229 (class 1259 OID 24944)
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
-- TOC entry 4993 (class 0 OID 0)
-- Dependencies: 229
-- Name: opinion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opinion_id_seq OWNED BY public.opinion.id;


--
-- TOC entry 228 (class 1259 OID 24931)
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
-- TOC entry 227 (class 1259 OID 24930)
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
-- TOC entry 4994 (class 0 OID 0)
-- Dependencies: 227
-- Name: pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pago_id_seq OWNED BY public.pago.id;


--
-- TOC entry 224 (class 1259 OID 24898)
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
    imagen text,
    pais text,
    favorita boolean DEFAULT false,
    ciudad character varying(50),
    provincia character varying(50),
    precio_por_noche numeric(10,2),
    descripcion text,
    capacidad_personas integer,
    tipo_propiedad character varying(50),
    activo boolean DEFAULT true,
    CONSTRAINT propiedad_cantidad_ambientes_check CHECK ((cantidad_ambientes >= 1))
);


ALTER TABLE public.propiedad OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24897)
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
-- TOC entry 4995 (class 0 OID 0)
-- Dependencies: 223
-- Name: propiedad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.propiedad_id_seq OWNED BY public.propiedad.id;


--
-- TOC entry 226 (class 1259 OID 24913)
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
-- TOC entry 225 (class 1259 OID 24912)
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
-- TOC entry 4996 (class 0 OID 0)
-- Dependencies: 225
-- Name: reserva_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;


--
-- TOC entry 4777 (class 2604 OID 24874)
-- Name: administrador id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador ALTER COLUMN id SET DEFAULT nextval('public.administrador_id_seq'::regclass);


--
-- TOC entry 4778 (class 2604 OID 24883)
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- TOC entry 4779 (class 2604 OID 24892)
-- Name: encargado id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado ALTER COLUMN id SET DEFAULT nextval('public.encargado_id_seq'::regclass);


--
-- TOC entry 4789 (class 2604 OID 24968)
-- Name: imagen id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen ALTER COLUMN id SET DEFAULT nextval('public.imagen_id_seq'::regclass);


--
-- TOC entry 4788 (class 2604 OID 24948)
-- Name: opinion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion ALTER COLUMN id SET DEFAULT nextval('public.opinion_id_seq'::regclass);


--
-- TOC entry 4786 (class 2604 OID 24934)
-- Name: pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago ALTER COLUMN id SET DEFAULT nextval('public.pago_id_seq'::regclass);


--
-- TOC entry 4780 (class 2604 OID 24901)
-- Name: propiedad id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad ALTER COLUMN id SET DEFAULT nextval('public.propiedad_id_seq'::regclass);


--
-- TOC entry 4785 (class 2604 OID 24916)
-- Name: reserva id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);


--
-- TOC entry 4969 (class 0 OID 24871)
-- Dependencies: 218
-- Data for Name: administrador; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrador (id, nombre, apellido, email, password) FROM stdin;
2	Carlos	Pérez	carlos@admin.com	admin456
1	Lucía Anabela	Gómez	lucia@admin.com	admin123
\.


--
-- TOC entry 4971 (class 0 OID 24880)
-- Dependencies: 220
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (id, nombre, apellido, email, password, dni, telefono, numero_tarjeta, nacionalidad) FROM stdin;
3	Adrian alejandro	Sambido	adriinform2021@gmail.com	clave3	\N	\N	\N	\N
4	Mariel	Ajala	mariela@cliente.com	clave4	\N	\N	\N	\N
6	Alejandro	Pozati	alejandro@cliente.com	clave6	18222555	-1	3333555566667776	Argentino
7	Pato	Verón	pato@cliente.com	clave	6666666	2222222	55451215	Paraguayo
8	Aacundo	Arana	facundo@encargado.com	caleve5	18251258	5785752872	3333555566667777	uruguayo
9	Soynuevo	Nuevo	nuevo@cliente.com	Clave888	18251258	02215623325	3333555566667777	Argentino
5	Nicolas	Viviers	nicolas@cliente.com	Clave555	52636362	2214563658	1111222233334444	Ucraniano
2	Juan	Martinez	juan@cliente.com	Clave222	20365365	2215645987	1111222233334444	Exrumano
1	Maria	Lopez	maria@cliente.com	Clave123	20651350	2214563658	6666333344445555	Argentina
10	Alejandro	Sambido	adrian.sambido40911@alumnos.info.unlp.edu.ar	Clave111	18251258	2214563658	6666333344445555	Argentino
\.


--
-- TOC entry 4973 (class 0 OID 24889)
-- Dependencies: 222
-- Data for Name: encargado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.encargado (id, nombre, apellido, email, password) FROM stdin;
2	Pedro	Sosa	pedro@encargado.com	enc456
1	Ana	Ramírez	ana@encargado.com	enc123
3	greta	piacentini	greta@encargado.com	enc123
4	Nicolás	Vieires	nicolas@encargado.com	enc222
\.


--
-- TOC entry 4983 (class 0 OID 24965)
-- Dependencies: 232
-- Data for Name: imagen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.imagen (id, url, propiedad_id) FROM stdin;
1	img/img1.avif	10
2	img/img2.jpg	6
3	img/img6.avif	7
4	img/img2.jpg	8
5	img/IMG4.avif	2
6	img/apartment-portada.jpg	9
7	img/img8.avif	1
\.


--
-- TOC entry 4981 (class 0 OID 24945)
-- Dependencies: 230
-- Data for Name: opinion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opinion (id, comentario, cantidad_estrellas, cliente_id, propiedad_id) FROM stdin;
1	Muy linda propiedad, todo limpio.	5	1	1
2	Buena ubicación pero algo ruidosa.	3	2	2
\.


--
-- TOC entry 4979 (class 0 OID 24931)
-- Dependencies: 228
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pago (id, reserva_id, monto, completado) FROM stdin;
1	1	50000.00	t
2	2	45000.00	f
\.


--
-- TOC entry 4975 (class 0 OID 24898)
-- Dependencies: 224
-- Data for Name: propiedad; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.propiedad (id, dpto, piso, numero, calle, cantidad_ambientes, petfriendly, listada, encargado_id, imagen, pais, favorita, ciudad, provincia, precio_por_noche, descripcion, capacidad_personas, tipo_propiedad, activo) FROM stdin;
10	2	1°	2035	7	3	f	t	3	\N	Argentina	f	La Plata	Buenos Aires	30.00	vacio	2	Departamento	t
6	--	--	4628	176	\N	f	t	2	\N	Argentina	f	Berisso	Buenos Aires	50.00	cochera, parrilla	5	casa	f
7	--	--	4628	28	\N	f	t	2	\N	Argentina	f	Berisso	Buenos Aires	50.00	cochera, parrilla	5	casa	f
8	--	None	2657	None	\N	f	t	2	\N	Argentina	f	Berisso	Buenos Aires	60.00	Patio amplio, cochera, parrilla .	4	casa	t
2	B	1	202	Av. Siempre Viva	3	f	t	2	\N	\N	f	Calafate	Santa Cruz	\N	Hotel lujoso	\N	\N	t
9	6	1°	120	Miterrant	2	t	t	3	\N	Francia	f	Bourges	Berry	60.00	Amplio, comodo, iluminado	3	Departamento	t
1	A	3	101	Calle Falsa	2	t	t	1	\N	\N	f	Más Falsa que la calle	Re Falsa	\N	Nadie le cree, ...por falsa	\N	\N	t
\.


--
-- TOC entry 4977 (class 0 OID 24913)
-- Dependencies: 226
-- Data for Name: reserva; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reserva (id, fecha_in, fecha_out, cliente_id, propiedad_id) FROM stdin;
1	2025-06-01	2025-06-07	1	1
2	2025-07-10	2025-07-15	2	2
\.


--
-- TOC entry 4997 (class 0 OID 0)
-- Dependencies: 217
-- Name: administrador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administrador_id_seq', 1, false);


--
-- TOC entry 4998 (class 0 OID 0)
-- Dependencies: 219
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_seq', 10, true);


--
-- TOC entry 4999 (class 0 OID 0)
-- Dependencies: 221
-- Name: encargado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.encargado_id_seq', 4, true);


--
-- TOC entry 5000 (class 0 OID 0)
-- Dependencies: 231
-- Name: imagen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.imagen_id_seq', 7, true);


--
-- TOC entry 5001 (class 0 OID 0)
-- Dependencies: 229
-- Name: opinion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opinion_id_seq', 1, false);


--
-- TOC entry 5002 (class 0 OID 0)
-- Dependencies: 227
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pago_id_seq', 1, false);


--
-- TOC entry 5003 (class 0 OID 0)
-- Dependencies: 223
-- Name: propiedad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.propiedad_id_seq', 10, true);


--
-- TOC entry 5004 (class 0 OID 0)
-- Dependencies: 225
-- Name: reserva_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reserva_id_seq', 1, false);


--
-- TOC entry 4795 (class 2606 OID 24878)
-- Name: administrador administrador_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_email_key UNIQUE (email);


--
-- TOC entry 4797 (class 2606 OID 24876)
-- Name: administrador administrador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (id);


--
-- TOC entry 4799 (class 2606 OID 24887)
-- Name: cliente cliente_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_email_key UNIQUE (email);


--
-- TOC entry 4801 (class 2606 OID 24885)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- TOC entry 4803 (class 2606 OID 24896)
-- Name: encargado encargado_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_email_key UNIQUE (email);


--
-- TOC entry 4805 (class 2606 OID 24894)
-- Name: encargado encargado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_pkey PRIMARY KEY (id);


--
-- TOC entry 4815 (class 2606 OID 24972)
-- Name: imagen imagen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_pkey PRIMARY KEY (id);


--
-- TOC entry 4813 (class 2606 OID 24953)
-- Name: opinion opinion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_pkey PRIMARY KEY (id);


--
-- TOC entry 4811 (class 2606 OID 24938)
-- Name: pago pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_pkey PRIMARY KEY (id);


--
-- TOC entry 4807 (class 2606 OID 24906)
-- Name: propiedad propiedad_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_pkey PRIMARY KEY (id);


--
-- TOC entry 4809 (class 2606 OID 24919)
-- Name: reserva reserva_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id);


--
-- TOC entry 4822 (class 2606 OID 24973)
-- Name: imagen imagen_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);


--
-- TOC entry 4820 (class 2606 OID 24954)
-- Name: opinion opinion_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id);


--
-- TOC entry 4821 (class 2606 OID 24959)
-- Name: opinion opinion_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opinion
    ADD CONSTRAINT opinion_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);


--
-- TOC entry 4819 (class 2606 OID 24939)
-- Name: pago pago_reserva_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pago_reserva_id_fkey FOREIGN KEY (reserva_id) REFERENCES public.reserva(id) ON DELETE CASCADE;


--
-- TOC entry 4816 (class 2606 OID 24907)
-- Name: propiedad propiedad_encargado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_encargado_id_fkey FOREIGN KEY (encargado_id) REFERENCES public.encargado(id);


--
-- TOC entry 4817 (class 2606 OID 24920)
-- Name: reserva reserva_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id);


--
-- TOC entry 4818 (class 2606 OID 24925)
-- Name: reserva reserva_propiedad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);


-- Completed on 2025-06-18 13:04:47

--
-- PostgreSQL database dump complete
--

