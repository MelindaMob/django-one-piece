-- Script SQL pour initialiser l'utilisateur Oracle
-- À exécuter dans le conteneur Oracle après le démarrage

-- Se connecter en tant que sysdba
-- sqlplus sys/oracle@localhost:1521/XE as sysdba

-- Créer l'utilisateur (si nécessaire)
CREATE USER opkb_user IDENTIFIED BY opkb_pass;
GRANT CONNECT, RESOURCE, DBA TO opkb_user;
GRANT UNLIMITED TABLESPACE TO opkb_user;

-- Alternative: utiliser l'utilisateur SYSTEM par défaut
-- Les migrations Django créeront automatiquement les tables

