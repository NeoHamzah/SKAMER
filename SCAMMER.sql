PGDMP  /    	        	        {         
   sewaKamera    16.1    16.1 "               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            	           1262    16398 
   sewaKamera    DATABASE     �   CREATE DATABASE "sewaKamera" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE "sewaKamera";
                postgres    false            �            1259    16400    admin    TABLE     �   CREATE TABLE public.admin (
    id_admin integer NOT NULL,
    username_admin character varying NOT NULL,
    password_admin character varying NOT NULL
);
    DROP TABLE public.admin;
       public         heap    postgres    false            �            1259    16399    admin_id_admin_seq    SEQUENCE     �   CREATE SEQUENCE public.admin_id_admin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.admin_id_admin_seq;
       public          postgres    false    216            
           0    0    admin_id_admin_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.admin_id_admin_seq OWNED BY public.admin.id_admin;
          public          postgres    false    215            �            1259    16409    barang    TABLE     �   CREATE TABLE public.barang (
    id_barang integer NOT NULL,
    nama_barang character varying NOT NULL,
    layanan_id integer NOT NULL,
    status_barang character varying NOT NULL,
    harga_sewa integer NOT NULL
);
    DROP TABLE public.barang;
       public         heap    postgres    false            �            1259    16418    layanan    TABLE     n   CREATE TABLE public.layanan (
    id_layanan integer NOT NULL,
    nama_layanan character varying NOT NULL
);
    DROP TABLE public.layanan;
       public         heap    postgres    false            �            1259    16417    layanan_id_layanan_seq    SEQUENCE     �   CREATE SEQUENCE public.layanan_id_layanan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.layanan_id_layanan_seq;
       public          postgres    false    220                       0    0    layanan_id_layanan_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.layanan_id_layanan_seq OWNED BY public.layanan.id_layanan;
          public          postgres    false    219            �            1259    16432 	   pemesanan    TABLE     
  CREATE TABLE public.pemesanan (
    id_pemesanan integer NOT NULL,
    nama_pemesan character varying NOT NULL,
    barang_id integer NOT NULL,
    durasi_sewa integer NOT NULL,
    tanggal_sewa date NOT NULL,
    tanggal_kembali date NOT NULL,
    biaya integer
);
    DROP TABLE public.pemesanan;
       public         heap    postgres    false            �            1259    16431    pemesanan_id_pemesanan_seq    SEQUENCE     �   CREATE SEQUENCE public.pemesanan_id_pemesanan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.pemesanan_id_pemesanan_seq;
       public          postgres    false    222                       0    0    pemesanan_id_pemesanan_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.pemesanan_id_pemesanan_seq OWNED BY public.pemesanan.id_pemesanan;
          public          postgres    false    221            �            1259    16408    stock_id_barang_seq    SEQUENCE     �   CREATE SEQUENCE public.stock_id_barang_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.stock_id_barang_seq;
       public          postgres    false    218                       0    0    stock_id_barang_seq    SEQUENCE OWNED BY     L   ALTER SEQUENCE public.stock_id_barang_seq OWNED BY public.barang.id_barang;
          public          postgres    false    217            _           2604    16403    admin id_admin    DEFAULT     p   ALTER TABLE ONLY public.admin ALTER COLUMN id_admin SET DEFAULT nextval('public.admin_id_admin_seq'::regclass);
 =   ALTER TABLE public.admin ALTER COLUMN id_admin DROP DEFAULT;
       public          postgres    false    215    216    216            `           2604    16412    barang id_barang    DEFAULT     s   ALTER TABLE ONLY public.barang ALTER COLUMN id_barang SET DEFAULT nextval('public.stock_id_barang_seq'::regclass);
 ?   ALTER TABLE public.barang ALTER COLUMN id_barang DROP DEFAULT;
       public          postgres    false    217    218    218            a           2604    16421    layanan id_layanan    DEFAULT     x   ALTER TABLE ONLY public.layanan ALTER COLUMN id_layanan SET DEFAULT nextval('public.layanan_id_layanan_seq'::regclass);
 A   ALTER TABLE public.layanan ALTER COLUMN id_layanan DROP DEFAULT;
       public          postgres    false    219    220    220            b           2604    16435    pemesanan id_pemesanan    DEFAULT     �   ALTER TABLE ONLY public.pemesanan ALTER COLUMN id_pemesanan SET DEFAULT nextval('public.pemesanan_id_pemesanan_seq'::regclass);
 E   ALTER TABLE public.pemesanan ALTER COLUMN id_pemesanan DROP DEFAULT;
       public          postgres    false    222    221    222            �          0    16400    admin 
   TABLE DATA           I   COPY public.admin (id_admin, username_admin, password_admin) FROM stdin;
    public          postgres    false    216   �%       �          0    16409    barang 
   TABLE DATA           _   COPY public.barang (id_barang, nama_barang, layanan_id, status_barang, harga_sewa) FROM stdin;
    public          postgres    false    218   �%                 0    16418    layanan 
   TABLE DATA           ;   COPY public.layanan (id_layanan, nama_layanan) FROM stdin;
    public          postgres    false    220   �&                 0    16432 	   pemesanan 
   TABLE DATA           }   COPY public.pemesanan (id_pemesanan, nama_pemesan, barang_id, durasi_sewa, tanggal_sewa, tanggal_kembali, biaya) FROM stdin;
    public          postgres    false    222   '                  0    0    admin_id_admin_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.admin_id_admin_seq', 1, true);
          public          postgres    false    215                       0    0    layanan_id_layanan_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.layanan_id_layanan_seq', 3, true);
          public          postgres    false    219                       0    0    pemesanan_id_pemesanan_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.pemesanan_id_pemesanan_seq', 14, false);
          public          postgres    false    221                       0    0    stock_id_barang_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.stock_id_barang_seq', 12, true);
          public          postgres    false    217            d           2606    16407    admin admin_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id_admin);
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public            postgres    false    216            h           2606    16425    layanan layanan_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.layanan
    ADD CONSTRAINT layanan_pkey PRIMARY KEY (id_layanan);
 >   ALTER TABLE ONLY public.layanan DROP CONSTRAINT layanan_pkey;
       public            postgres    false    220            j           2606    16439    pemesanan pemesanan_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.pemesanan
    ADD CONSTRAINT pemesanan_pkey PRIMARY KEY (id_pemesanan);
 B   ALTER TABLE ONLY public.pemesanan DROP CONSTRAINT pemesanan_pkey;
       public            postgres    false    222            f           2606    16416    barang stock_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.barang
    ADD CONSTRAINT stock_pkey PRIMARY KEY (id_barang);
 ;   ALTER TABLE ONLY public.barang DROP CONSTRAINT stock_pkey;
       public            postgres    false    218            l           2606    16440    pemesanan barang_id    FK CONSTRAINT     |   ALTER TABLE ONLY public.pemesanan
    ADD CONSTRAINT barang_id FOREIGN KEY (barang_id) REFERENCES public.barang(id_barang);
 =   ALTER TABLE ONLY public.pemesanan DROP CONSTRAINT barang_id;
       public          postgres    false    4710    218    222            k           2606    16426    barang layanan_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.barang
    ADD CONSTRAINT layanan_id FOREIGN KEY (layanan_id) REFERENCES public.layanan(id_layanan) NOT VALID;
 ;   ALTER TABLE ONLY public.barang DROP CONSTRAINT layanan_id;
       public          postgres    false    4712    218    220            �      x�3�L,���442�����  S4      �   �   x�]��n�0E�㯘/�l^&�(��&ؕB_R64X�H4F�J���:,G�\�Gp���	�����jX�3gl�J+癏��3�؍8����'��dN����fI�C��M y*�b_�{%ݜ!aoΗߨ1���5OgZ��t_v��9e5+;0��/�N��:���z2m��ų�Ư����NJ{��[j��x{3�G���[�����d�7w��<>0�� ��o`         -   x�3�N-OTpN�M-J�2��|R���!���̂��=... B�6         �   x�u�=�0�ٹKQl7'@b`bAbɂT	���$N���[�/�{F8N%Y�i�a}&@��ZCP�{~ 6���k�U�d?I��"�^���˿.n3&��;*s2-tւ(�H��\fp�t+C���RwQuKߺ���N�����yz����$a����B��O$U�.oc��0c?     