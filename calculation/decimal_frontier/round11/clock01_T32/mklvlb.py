s = open("lvl2.cpp").read()
a = """    { bool nw; tab.insert(0 | (bd << W) | (br << (2 * W)), &nw); }"""
b = """    // r11b lvlb: AIN=dir loads the stored forward closure A'_W(ph) (written by lvl2 with NOBWD=1) instead of recomputing it;
    // only the backward fixpoint (co-reachability inside A'_W(ph)) is run. Result identical to lvl2 without NOBWD.
    const char* ain = getenv("AIN");
    if (ain) { string fn = wh::lname(ain, B, PAT, W, ph); int fd = open(fn.c_str(), O_RDONLY); if (fd < 0) { fprintf(stderr, "missing %s\\n", fn.c_str()); return 2; }
      struct stat st; fstat(fd, &st); u64 n = st.st_size / 8; const u64* p = (const u64*)mmap(nullptr, n * 8, PROT_READ, MAP_SHARED, fd, 0); close(fd);
      vector<thread> th; for (int i = 0; i < nth; i++) th.emplace_back([&, i]() { bool nw; for (u64 j = n * i / nth; j < n * (i + 1) / nth; j++) tab.insert(p[j], &nw); });
      for (auto& x : th) x.join(); munmap((void*)p, n * 8);
      printf("loaded A' w=%d ph=%d from %s: %llu windows\\n", W, ph, fn.c_str(), (unsigned long long)tab.n.load()); fflush(stdout);
    } else
    { bool nw; tab.insert(0 | (bd << W) | (br << (2 * W)), &nw); }"""
assert s.count(a) == 1
s = s.replace(a, b)
a2 = "    while (true) {\n      atomic<u64> next{0}, expanded{0}, cut{0};"
assert s.count(a2) == 1
s = s.replace(a2, "    while (!ain) {\n      atomic<u64> next{0}, expanded{0}, cut{0};")
open("lvlb.cpp", "w").write(s)
print("ok")
