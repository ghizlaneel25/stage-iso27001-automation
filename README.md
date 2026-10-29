# 🛡️ Automatisation de l'Audit ISO/IEC 27001

## 📌 Description

Système d'audit automatisé pour vérifier la conformité d'un serveur Ubuntu aux contrôles de sécurité des annexes **A.5 (organisationnels)** et **A.8 (technologiques)** de la norme ISO/IEC 27001:2022.

Projet réalisé dans le cadre d'un stage d'été à la **Caisse Marocaine des Retraites (CMR)**.

---

## 🏗️ Architecture

Le système repose sur une architecture à deux machines virtuelles communiquant de manière sécurisée via SSH.

```mermaid
graph LR
    subgraph Kali Linux [Poste de Contrôle - Kali Linux]
        A[Scripts Python] --> B[(Base SQLite)]
        A --> C[Dashboard Streamlit]
    end

    subgraph Ubuntu Server [Cible Auditée - Ubuntu Server]
        D[OpenSCAP]
        E[Lynis]
        F[Services Système<br>auditd, chrony, nftables]
    end

    A -- Connexion SSH (Paramiko) --> D
    A -- Connexion SSH (Paramiko) --> E
    A -- Connexion SSH (Paramiko) --> F
    
    D -. Résultats .-> B
    E -. Résultats .-> B
    F -. Résultats .-> B

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|-------------|------|
| **Python 3** | Langage des scripts d'audit |
| **Paramiko** | Connexion SSH sécurisée |
| **OpenSCAP** | Audit de conformité CIS Benchmark |
| **Lynis** | Score de durcissement (Hardening Index) |
| **Streamlit** | Dashboard interactif |
| **SQLite** | Base de données des résultats |
| **LaTeX** | Génération du rapport |

---

## 📊 Résultats

| Métrique | Valeur |
|----------|--------|
| **Contrôles couverts** | 71 (100% du périmètre A.5 + A.8) |
| **Contrôles automatisés** | 30 |
| **Contrôles manuels** | 41 |
| **Score global** | 53,8% (42/70 conformes) |
| **Score OpenSCAP** | 73,12% |

---

## 📁 Structure du projet
stage-iso27001-automation/
├── controls/ # Scripts des 71 contrôles
│ ├── A.5.x-/ # Contrôles organisationnels
│ └── A.8.x-/ # Contrôles technologiques
├── dashboard/ # Dashboard Streamlit
│ ├── app.py
│ └── data_loader.py
├── db/ # Base SQLite (exclue du repo)
├── scan-results/ # Rapports OpenSCAP/Lynis (exclus)
├── rapport/ # Rapport LaTeX
├── template_manuel.py # Template de saisie manuelle
└── export_excel_final.py # Génération de l'Excel



