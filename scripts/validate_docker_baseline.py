#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys
SENSITIVE_ENV_PATTERNS=[re.compile(r"(?i)^\s*ENV\s+.*(?:PASSWORD|TOKEN|SECRET|API_KEY)\s*=",re.M),re.compile(r"(?i)^\s*ARG\s+.*(?:PASSWORD|TOKEN|SECRET|API_KEY)\s*=",re.M)]
EMBED=re.compile(r"(?i)(apt|apk|yum|dnf).*(postgresql-server|postgresql\b)")
def main():
 p=argparse.ArgumentParser();p.add_argument("dockerfile");p.add_argument("--dockerignore");a=p.parse_args();t=Path(a.dockerfile).read_text();e=[]
 fs=re.findall(r"^\s*FROM\s+(\S+)",t,re.M|re.I)
 if not fs:e.append("missing FROM")
 for im in fs:
  if im.lower().endswith(":latest") or ":" not in im.split("@")[0]:e.append(f"base image must use explicit version/tag: {im}")
 if not re.search(r"^\s*WORKDIR\s+\S+",t,re.M|re.I):e.append("missing WORKDIR")
 if not re.search(r"^\s*USER\s+\S+",t,re.M|re.I):e.append("missing USER")
 if not re.search(r"^\s*(ENTRYPOINT|CMD)\s+",t,re.M|re.I):e.append("missing ENTRYPOINT/CMD")
 if re.search(r"^\s*COPY\s+\.\s+/\s*$",t,re.M|re.I):e.append("unsafe COPY . /")
 if EMBED.search(t):e.append("app image must not install PostgreSQL server")
 for pat in SENSITIVE_ENV_PATTERNS:
  if pat.search(t):e.append("secret-like ENV/ARG declaration detected")
 if a.dockerignore:
  x=Path(a.dockerignore).read_text() if Path(a.dockerignore).exists() else ""
  for req in [".git",".env","*.zip"]:
   if req not in x:e.append(f".dockerignore missing: {req}")
 if e:
  print("FAIL");[print("-",x) for x in e];return 1
 print(f"PASS: Docker baseline valid ({len(fs)} stage(s))");return 0
if __name__=="__main__":sys.exit(main())
