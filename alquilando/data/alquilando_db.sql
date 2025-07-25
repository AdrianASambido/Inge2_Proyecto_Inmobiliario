PGDMP  -    9                }         
   Alquilando    17.5    17.5 8    9           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            :           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            ;           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            <           1262    16608 
   Alquilando    DATABASE     �   CREATE DATABASE "Alquilando" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Argentina.1252';
    DROP DATABASE "Alquilando";
                     postgres    false            �            1259    16826    administrador    TABLE     *  CREATE TABLE public.administrador (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    rol character varying(20) DEFAULT 'admin'::character varying,
    intentos_fallidos integer,
    bloqueado_hasta timestamp without time zone
);
 !   DROP TABLE public.administrador;
       public         heap r       postgres    false            �            1259    16825    administrador_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administrador_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.administrador_id_seq;
       public               postgres    false    218            =           0    0    administrador_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.administrador_id_seq OWNED BY public.administrador.id;
          public               postgres    false    217            �            1259    16957    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    16835    cliente    TABLE     �  CREATE TABLE public.cliente (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    rol character varying(20) DEFAULT 'cliente'::character varying,
    intentos_fallidos integer,
    bloqueado_hasta timestamp without time zone,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    dni character varying(10) NOT NULL,
    telefono character varying(20),
    direccion character varying(200) NOT NULL,
    ciudad character varying(100) NOT NULL,
    pais character varying(100) NOT NULL,
    nro_tarjeta character varying(16),
    nombre_titular character varying(100),
    vencimiento_tarjeta character varying(5),
    cvv character varying(4)
);
    DROP TABLE public.cliente;
       public         heap r       postgres    false            �            1259    16834    cliente_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.cliente_id_seq;
       public               postgres    false    220            >           0    0    cliente_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;
          public               postgres    false    219            �            1259    16844 	   encargado    TABLE     *  CREATE TABLE public.encargado (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    rol character varying(20) DEFAULT 'encargado'::character varying,
    intentos_fallidos integer,
    bloqueado_hasta timestamp without time zone
);
    DROP TABLE public.encargado;
       public         heap r       postgres    false            �            1259    16843    encargado_id_seq    SEQUENCE     �   CREATE SEQUENCE public.encargado_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.encargado_id_seq;
       public               postgres    false    222            ?           0    0    encargado_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.encargado_id_seq OWNED BY public.encargado.id;
          public               postgres    false    221            �            1259    16920    imagen    TABLE     r   CREATE TABLE public.imagen (
    id integer NOT NULL,
    url text NOT NULL,
    propiedad_id integer NOT NULL
);
    DROP TABLE public.imagen;
       public         heap r       postgres    false            �            1259    16919    imagen_id_seq    SEQUENCE     �   CREATE SEQUENCE public.imagen_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.imagen_id_seq;
       public               postgres    false    228            @           0    0    imagen_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.imagen_id_seq OWNED BY public.imagen.id;
          public               postgres    false    227            �            1259    16853 	   propiedad    TABLE     L  CREATE TABLE public.propiedad (
    id integer NOT NULL,
    calle character varying(100) NOT NULL,
    ciudad character varying(100) NOT NULL,
    pais character varying(100) NOT NULL,
    cantidad_ambientes integer NOT NULL,
    petfriendly boolean DEFAULT false,
    listada boolean DEFAULT true,
    encargado_id integer,
    precio_noche double precision,
    numero character varying(10) NOT NULL,
    provincia character varying(100) NOT NULL,
    codigo_postal character varying(20) NOT NULL,
    CONSTRAINT propiedad_cantidad_ambientes_check CHECK ((cantidad_ambientes >= 1))
);
    DROP TABLE public.propiedad;
       public         heap r       postgres    false            �            1259    16852    propiedad_id_seq    SEQUENCE     �   CREATE SEQUENCE public.propiedad_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.propiedad_id_seq;
       public               postgres    false    224            A           0    0    propiedad_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.propiedad_id_seq OWNED BY public.propiedad.id;
          public               postgres    false    223            �            1259    16868    reserva    TABLE     �   CREATE TABLE public.reserva (
    id integer NOT NULL,
    fecha_in date NOT NULL,
    fecha_out date NOT NULL,
    cliente_id integer NOT NULL,
    propiedad_id integer NOT NULL,
    CONSTRAINT fechas_validas CHECK ((fecha_in < fecha_out))
);
    DROP TABLE public.reserva;
       public         heap r       postgres    false            �            1259    16867    reserva_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reserva_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.reserva_id_seq;
       public               postgres    false    226            B           0    0    reserva_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.reserva_id_seq OWNED BY public.reserva.id;
          public               postgres    false    225            t           2604    16829    administrador id    DEFAULT     t   ALTER TABLE ONLY public.administrador ALTER COLUMN id SET DEFAULT nextval('public.administrador_id_seq'::regclass);
 ?   ALTER TABLE public.administrador ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            v           2604    16838 
   cliente id    DEFAULT     h   ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);
 9   ALTER TABLE public.cliente ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219    220            x           2604    16847    encargado id    DEFAULT     l   ALTER TABLE ONLY public.encargado ALTER COLUMN id SET DEFAULT nextval('public.encargado_id_seq'::regclass);
 ;   ALTER TABLE public.encargado ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    221    222            ~           2604    16923 	   imagen id    DEFAULT     f   ALTER TABLE ONLY public.imagen ALTER COLUMN id SET DEFAULT nextval('public.imagen_id_seq'::regclass);
 8   ALTER TABLE public.imagen ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    227    228    228            z           2604    16856    propiedad id    DEFAULT     l   ALTER TABLE ONLY public.propiedad ALTER COLUMN id SET DEFAULT nextval('public.propiedad_id_seq'::regclass);
 ;   ALTER TABLE public.propiedad ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223    224            }           2604    16871 
   reserva id    DEFAULT     h   ALTER TABLE ONLY public.reserva ALTER COLUMN id SET DEFAULT nextval('public.reserva_id_seq'::regclass);
 9   ALTER TABLE public.reserva ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225    226            +          0    16826    administrador 
   TABLE DATA           e   COPY public.administrador (id, email, password, rol, intentos_fallidos, bloqueado_hasta) FROM stdin;
    public               postgres    false    218   �D       6          0    16957    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    229   -E       -          0    16835    cliente 
   TABLE DATA           �   COPY public.cliente (id, email, password, rol, intentos_fallidos, bloqueado_hasta, nombre, apellido, dni, telefono, direccion, ciudad, pais, nro_tarjeta, nombre_titular, vencimiento_tarjeta, cvv) FROM stdin;
    public               postgres    false    220   WE       /          0    16844 	   encargado 
   TABLE DATA           a   COPY public.encargado (id, email, password, rol, intentos_fallidos, bloqueado_hasta) FROM stdin;
    public               postgres    false    222   1F       5          0    16920    imagen 
   TABLE DATA           7   COPY public.imagen (id, url, propiedad_id) FROM stdin;
    public               postgres    false    228   �F       1          0    16853 	   propiedad 
   TABLE DATA           �   COPY public.propiedad (id, calle, ciudad, pais, cantidad_ambientes, petfriendly, listada, encargado_id, precio_noche, numero, provincia, codigo_postal) FROM stdin;
    public               postgres    false    224   eJ       3          0    16868    reserva 
   TABLE DATA           T   COPY public.reserva (id, fecha_in, fecha_out, cliente_id, propiedad_id) FROM stdin;
    public               postgres    false    226   	N       C           0    0    administrador_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.administrador_id_seq', 1, false);
          public               postgres    false    217            D           0    0    cliente_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.cliente_id_seq', 1, false);
          public               postgres    false    219            E           0    0    encargado_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.encargado_id_seq', 4, true);
          public               postgres    false    221            F           0    0    imagen_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.imagen_id_seq', 1, false);
          public               postgres    false    227            G           0    0    propiedad_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.propiedad_id_seq', 56, true);
          public               postgres    false    223            H           0    0    reserva_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.reserva_id_seq', 1, false);
          public               postgres    false    225            �           2606    16833 %   administrador administrador_email_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_email_key UNIQUE (email);
 O   ALTER TABLE ONLY public.administrador DROP CONSTRAINT administrador_email_key;
       public                 postgres    false    218            �           2606    16831     administrador administrador_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.administrador DROP CONSTRAINT administrador_pkey;
       public                 postgres    false    218            �           2606    16961 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    229            �           2606    16842    cliente cliente_email_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_email_key UNIQUE (email);
 C   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_email_key;
       public                 postgres    false    220            �           2606    16840    cliente cliente_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_pkey;
       public                 postgres    false    220            �           2606    16851    encargado encargado_email_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_email_key UNIQUE (email);
 G   ALTER TABLE ONLY public.encargado DROP CONSTRAINT encargado_email_key;
       public                 postgres    false    222            �           2606    16849    encargado encargado_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.encargado
    ADD CONSTRAINT encargado_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.encargado DROP CONSTRAINT encargado_pkey;
       public                 postgres    false    222            �           2606    16927    imagen imagen_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.imagen DROP CONSTRAINT imagen_pkey;
       public                 postgres    false    228            �           2606    16861    propiedad propiedad_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.propiedad DROP CONSTRAINT propiedad_pkey;
       public                 postgres    false    224            �           2606    16874    reserva reserva_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_pkey;
       public                 postgres    false    226            �           2606    16928    imagen imagen_propiedad_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.imagen
    ADD CONSTRAINT imagen_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);
 I   ALTER TABLE ONLY public.imagen DROP CONSTRAINT imagen_propiedad_id_fkey;
       public               postgres    false    228    224    4750            �           2606    16862 %   propiedad propiedad_encargado_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.propiedad
    ADD CONSTRAINT propiedad_encargado_id_fkey FOREIGN KEY (encargado_id) REFERENCES public.encargado(id);
 O   ALTER TABLE ONLY public.propiedad DROP CONSTRAINT propiedad_encargado_id_fkey;
       public               postgres    false    224    222    4748            �           2606    16875    reserva reserva_cliente_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id);
 I   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_cliente_id_fkey;
       public               postgres    false    4744    220    226            �           2606    16880 !   reserva reserva_propiedad_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_propiedad_id_fkey FOREIGN KEY (propiedad_id) REFERENCES public.propiedad(id);
 K   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_propiedad_id_fkey;
       public               postgres    false    4750    226    224            +   :   x�3�LN,��/vHL����K����LL� N�?.CΜ���DtU�F�Ȫb���� A��      6      x�KK2HJ1H15HL������� 22d      -   �   x�e��j1��_�/�f2��� +(Ud�BA�!��ҵпo��Ru��a����(/>���a�/g�$�A���1v+,�/�C_Y@d�a�2hk-�d����,�>�(J��4^rPo��k�|,y��RD?!C
c�ڹS�m�[MOf\����t�8��-���C0P]������ƶ�����?�b�Vj����?l7�����WC      /   ]   x�3�L�KtH�KN,JOL��K������9ႜ�1~\F��)E��jML���s�&%�c*63�@Wl��Z\��������ј�c���� j�9<      5   �  x���Mn�F��������`�"�P�G�X�\?�\@�占$�}��H��v�|�����}�������Ϗ��Ϸ������v����B�g�e�����s�������z��ޟ���ۏ��ӿ������oedk1B���r�����kۈF�AW�f�R�r�]N�6{{8@�܀&:�w��xl���|���� Cp�eٯ�.]rX?�{AHj@�m���[�E�&�u���3ptn@��>ݛ-��)bݺgԀ�9C[_6���[��ã'&u��1č���z�N�k<�>�Q�-���ϥm���D�sc�YW�%�8�͓mz~8aB(�c섅�h��u�>�*����X���i:Ԗ��ɯ�,k{|#D �u�)����3GtYz����$ �e�IB8����خ�O����?�P�� �A)���}���.+P�=��T�rh����.;PJ�]w�&�C���u�vف:`�e�qt�h�=���}���9�ơ]v��B��@s�vف0�]v�%�\ȫ���.;��B��@�p�����|]u��L�U���9����dʮ:���]s��C��@O8�v݁��e�@�i��@�r'�:0�C��_PdaD��YՀ� �vY�2jW���A���:�ú&���.�o"�U��'�]V��L��P��*^��A]W�#)��P�,��5`"ɔ]�;:���5�@��׀�L�UjC��P�C�^*��n�xh�����ɔ]��\��5`�sh�k��q����o`�Z��d�.�nd�.���z�d�.׀���]��C�^Ʊn�x����c�)�\Lr%/׀�C��@o���|v�&Y��k@�$sv9&��5�c���k��$�v�LL��b��k��z8�����E��g���T5<�+� 7      1   �  x��W�N�0]�_�/@q켖m��
Sb�42�����$,�O,F�	���y�r�T�������4&K���y0�]�A��LD����ě0A(ْ�x��P�%�Rf:w��ȼZpg�K���Rf�̄Q���ߍ�6J ��?z���$+�,M!�����o�J�&��j�az�G.7�H�����g���$����`䇑�	�
�-ż4��Z��ܼ�6 (�b��%��#�t��ɕΒ҈����:+������UzF;¶�����ϰ��d;�v^i��P��5T0`����2/T�]W �'�������ߚ�as��9�^�������(���h��#� W�]��C��a���l��uhk�"`�͎e��_�^�'�b=���6�������(f9�F&>�a�Y�v!r��������G}dpa�턭f>��e
I�XJ��v�b��]r��g�a��̅4��IP?�DV��J`v�"|�`��I��G���o�r�� �D����h��2�@��so�Fn��C�>Y�g��~+0��¬[r�b:k��7w��p� Շ3�&��v��Hn1�7�Q���]뺟��wMd���d���Z�n�I9y���xmX�ujEh���3��r�9�����w"���`��E_�2�g�Q� m�(r��ʤo*�Ν~�V��������+���ej�h+�_����L�;̙�(M"�m�h�y�qw�D:k%�]��'9�W�����m�+P�rX������W��b��i�3�:aHV�Y��ȍ� ��WK���i����{����-�p���Y*�>�ZU^=%��Ƿj]:' �ȡ��|1�򓠅S�=x���+ɣ�T���N�GH\�Ǐ��3r�,�4���WO�L&b�Ώ����b6��P�      3   .   x�3�4202�50�50D0�99���溆�)'P�+F��� >	�     