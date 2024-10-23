# Onboard-Mate

## Initial setup
 `pyenv install 3.12.7`
 `pyenv local 3.12.7`
 `pyenv exec python -m venv venv`
 `source venv/bin/activate`
 `pip install -r requirements.txt`

To get started run - 

`streamlit run main.py`


## PROJECT TREE
```
Onboard-Mate
├─ .cache
│  ├─ 41
│  │  ├─ cache.db
│  │  ├─ cache.db-shm
│  │  └─ cache.db-wal
│  └─ 42
│     ├─ cache.db
│     ├─ cache.db-shm
│     └─ cache.db-wal
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  ├─ jerome_dev
│  │     │  ├─ main
│  │     │  ├─ pat_dev
│  │     │  └─ rohit_dev
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ HEAD
│  │           ├─ main
│  │           └─ pat_dev
│  ├─ objects
│  │  ├─ 00
│  │  │  └─ 3a92e30af5baa098fe93ee9e5f8093e0dac9a0
│  │  ├─ 04
│  │  │  └─ 0e10ac55fbfd3b199595457ccfa96009d474cc
│  │  ├─ 11
│  │  │  └─ fa7e4dba138657cafa040b0fac8b251b6a7228
│  │  ├─ 13
│  │  │  └─ c34a3494aa4a13f59c659a0207360895e1738c
│  │  ├─ 19
│  │  │  ├─ 8a97d6283a3eaa338ff55527239e53eca79998
│  │  │  └─ f72c693834b91b4aae50a60cb57792eb509b48
│  │  ├─ 24
│  │  │  └─ 68f6f9a2ce5153845746376ae528da93d7df8f
│  │  ├─ 29
│  │  │  ├─ 739d97693d7136da559f0c9e72626396be69f6
│  │  │  └─ 9e03139fddefd20e68822037ea1eb83c7a3a7f
│  │  ├─ 34
│  │  │  └─ 0de329c16e6b7bc94709709e390b76378edc0b
│  │  ├─ 36
│  │  │  └─ de897108c221a801608d209cafabc20bcb6d2a
│  │  ├─ 37
│  │  │  └─ 63a24fc7abd567fd0846a17f599b1f5d372356
│  │  ├─ 3e
│  │  │  └─ 1e144e9ba5e988b1d83777e24c43e13366aead
│  │  ├─ 43
│  │  │  └─ faaad167b9690da39baf5c7737ca3351580672
│  │  ├─ 44
│  │  │  └─ 1d0fcbcd14e8fa8327b88c3159af9fabe6754a
│  │  ├─ 46
│  │  │  └─ 64443d379afe67282f896fa8d754939fc08fd0
│  │  ├─ 49
│  │  │  └─ 480dd46272013bce55277efeaee307dd42e4fa
│  │  ├─ 4b
│  │  │  └─ 95a052cca8a0a340c63cfb29d5f75b6b6b3a33
│  │  ├─ 4d
│  │  │  └─ ad76e6761c567383cd8e34b79d848ba242bed7
│  │  ├─ 55
│  │  │  └─ 334b9f95abcbcc21fbe74439489963254af98c
│  │  ├─ 56
│  │  │  └─ bb66057d203263dd844452d716067976ccbefa
│  │  ├─ 5c
│  │  │  └─ eb3864c2911029f0a6010fadab352e4b8e2d07
│  │  ├─ 63
│  │  │  └─ 94243a005fca6df9320329bd0e5273c0ad1cae
│  │  ├─ 6c
│  │  │  └─ 85d381a744e6447defd0b0a0a63ce42b4cf95b
│  │  ├─ 74
│  │  │  └─ bdce8ce9dc320141234cfac33c51feed157e14
│  │  ├─ 75
│  │  │  └─ fe7b18256bbdc7f03420260a49ddbc3593cb21
│  │  ├─ 7a
│  │  │  └─ 1c13c4157e25249291de85f3f64a67162193aa
│  │  ├─ 7e
│  │  │  └─ 9d4981abfc68b45f181e9e369b32c8d55fe41d
│  │  ├─ 8f
│  │  │  └─ 66ae9bcb7333a6380e837210fd9084cff4e041
│  │  ├─ 9e
│  │  │  ├─ 04ea8228c0de2ca8e924380cc8c63649d3badb
│  │  │  └─ 803ef7bf67569ea9ecbf654285195f1ff10ada
│  │  ├─ 9f
│  │  │  └─ c3c433b854e267f50145070b4ec79278d87287
│  │  ├─ a0
│  │  │  └─ efa1d71be4a80f4b5f0abbeb98ba0ce62c2c25
│  │  ├─ ab
│  │  │  └─ b877bd6309641bb9ae3f1068aeedab65c567d5
│  │  ├─ ad
│  │  │  ├─ a21b5fa90c91e5033d6d82c91205d1bdc7da02
│  │  │  └─ fa7e4635ae3a449c3b8d9ce455b2d99f14b85a
│  │  ├─ ae
│  │  │  └─ f3303d56554f2c8ed43733c28d989a743b7306
│  │  ├─ c9
│  │  │  └─ 2d376937eee3ee28ac5dd85ab1db3fe333b415
│  │  ├─ d4
│  │  │  └─ 37995a15c0b3ceaf8a0741764705b2590e054d
│  │  ├─ dc
│  │  │  └─ 4b58b359da7daeecdf8828998214b515a9d5c0
│  │  ├─ e6
│  │  │  └─ 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
│  │  ├─ ea
│  │  │  └─ 1bcabc7add69a9aceb89c5700a20facde01c1c
│  │  ├─ f0
│  │  │  └─ 13e71b89240fe6f494f05858b69d42b011f2ce
│  │  ├─ fe
│  │  │  └─ 9ac2845eca6fe6da8a63cd096d9cf9e24ece10
│  │  ├─ ff
│  │  │  └─ 731501df9244c2367328e53e6c40c1514db6bf
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-bbe2e770cea24f749f096f480bb3c6e847d0386a.idx
│  │     └─ pack-bbe2e770cea24f749f096f480bb3c6e847d0386a.pack
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ jerome_dev
│     │  ├─ main
│     │  ├─ pat_dev
│     │  └─ rohit_dev
│     ├─ remotes
│     │  └─ origin
│     │     ├─ HEAD
│     │     ├─ main
│     │     └─ pat_dev
│     └─ tags
├─ .gitignore
├─ .python-version
├─ README.md
├─ autogen_module.py
├─ coding
├─ connection.py
├─ main.py
├─ requirements.txt
├─ schema_table.py
└─ transform.py

```