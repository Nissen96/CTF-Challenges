# Writeup

Download the intercepted network traffic PCAP file and the power trace from the TLS encryption.

Inspecting the PCAP, we find mostly TLS-encrypted traffic. There are some exceptions though, all from the same IP.

We see this client visits some sites over HTTP and if we follow the TCP streams, we find he connects to someone else with a direct TCP connection and has the following conversation:

```
#START CHAT#
#CHAT ACCEPTED#
#MSG# Sergiu, do you copy?
#MSG# General Red Eagle, this is an old and unencrypted channel, you are not supposed to use this, everything is encrypted now!
#MSG# I know that but I somehow disabled TLS support and now I cannot get my stupid computer to use it again - I don't have access to anything now!
#MSG# It is crucial I get my access back very soon, I have a very important email to send out.
#MSG# Should be a simple fix, I'll walk you through it.
#MSG# I have a certificate and private key on my desktop, should I send that?
#MSG# NO NO NO, I do NOT need that, PLEASE do NOT send that to ANYONE, and ESPECIALLY not an unencrypted channel!
#MSG# The RSA private key is used by the server to setup TLS sessions! Whoever has this can decrypt and see EVERYTHING
#MSG# Obviously yes, we have used the same key for all servers and services, so we can monitor everyone
#MSG# I'll come by your office and take a look before you accidentally leak the private key here...
#MSG# Alright, but come quick!
#END CHAT#
#CHAT ENDED#
```

From this, we see he was supposed to use TLS encryption for everything and has an RSA private key.

We would like to decrypt all the traffic as well, so we need to know how everything was encrypted.

We can look at any of the handshakes (specifically at the SERVER HELLOs) in the PCAP to find the encryption algorithm and certificate used. Here we see the ciphersuite used is `TLS_RSA_WITH_AES_256_GCM_SHA384`, so an RSA encryption as expected. Looking deeper into the certificate fields, we find the public key info:

```
modulus: 0x00acc6f68ff45b36db5a076379c470d70d0b19e73058158933aeb1d9cc1f370d267ee2f5f36c061c49fe02269fba69e3c8783eff9494f261638a604506260c076d280a94a691a373720958fd276af60925d48c027419b12048a4bc329fb87dd7e2b34a0573b6042d7e65a54cc846a47e3becd50c52ed3de5bca4c5609ed9aa4a65d8c13d342155f5eada14110c57f1390e1a074a9ffbc157f6c39dadf2190ddbb40a16a7dd0bbb636a7ef1cf475170f7a0b8d2b4b481fb1c8b9a514d5c71fcfeb6138705a11b8d6c1c795c23179b3d7533bf295621a7275c07d021e24843fd160a734552b56a277452a1d0c41fd8443b8c5a7b46944447e934d268705bd3b137af6e2eb36387eb3a68e0c8d8acc431d2cdee5e722cecba1ce96ee05ebc1d80b8a4eaf05749f33ef52dd58ca52b1eef2717b54729a04eacff1975b409f56044990cb6e24c4d0b0fac9e0192516d1eb70d8e9ee6cd03ad4c930f2e2e10ff206e52f3b4925602ed1cbacbdaa77fb9fb5b835d5ed9101444a1853007a2fdc084421b71adab5252639aa37b5b1a3ee99af2bdecfc3c5d6917b1291d898caf99cba36d0d8e0aa833775ab062f2424ca5da5250faa84877308da734884ec8725c557e2cfdd6272424ce7f25b05ee7ffbf82bad4a656f355086d033ddd1e23c381e483242be86b8a0f8f18d768f77941217a8821288edcedaca429a5f14a79a5b5f65b69d5

publicExponent: 65537
```

If we can find the private exponent as well, we can generate the correct RSA private key ourselves and get Wireshark to decrypt the traffic for us.

Luckily, we have been told we have a power trace of a TLS encryption, which must have used the private exponent. We can load in the stored Numpy array with `np.load` and inspect the power profile. Plotting a part of it with `matplotlib` (or looking at the included screenshot), we see a lot of fairly regular peaks. Some of them seem to be longer in duration and has a higher power consumption as well.

Knowing a bit about the RSA algorithm, we encrypt by raising to the private exponent, `d`. This is often done with the square and multiply algorithm where we iterate over each bit in the key and always square the result but only multiply when the bit is a 1.

So, what we are seeing is some high and wide peaks whenever both squaring and multiplicaiton is done, meaning it corresponds to a 1-bit. The smaller peaks correspond to a 0. We can thus basically just read the key bits from the graph - or more realistically, write some code to do it for us.

With some inspection and tweaking, we find that if we sample every 50 pixels (with an offset of something close to 25), we get one sample per peak (or lack of peak) and can get the entire key.

We find this to be

```
privateExponent: 0x67abcaee7dd4ed8998efae04b6966eb368e1d612f0079c17e2cedcbcda4e1219f331041b57ca22d7530ebf564068a140fcc5f05d9b3204b5d1a60a44b237ad8d15e5a3647f26f07290a150e5820cb75877bcbb0c270e5d2cb98c23642b33778293c9ea938fb7da0469c151dd2a6631488bc71a69f7e8981d255139b4972ed30d618e31c741e96e71c9011969aaab176d1ab91d51f9a1fdc21786598556fb35c545f86a28fc8d280e12b5cd86219c0339f12c9d396274e69fedacb31ab15af90b0f9489102e942136c4ab40733db716c841ffefaaa9bdb83f07e80cfb07b0a8b5048da81f2adf19b12b5f350f56993a91f108df44bfe3d64ed7a1cb298e505bf46ea7714dc9303134a303646b880af163dbcce935443ef5aa4842a92939da270cc53ee82b3381fcc04e705c1a4cebc426b1a2e05cc654fbb3f024f6f68d903f58198a070f6d0bcb710c1a24321841175417a0c2363dda2a863b33c668cd0ec33ee6f3aefcdee180c397d600a67ffea2075844f3a7b7b579c6185c1e1de0979a7bad0c89af9381aaecc09ac3c9eed04f7b4dbd651c722836f1f536cfe59fd8a80b91a20004da31cc69bd07412cfdf0c72f6837efd08e9fe497e4ffd1fe708b402035bc43787fa15ed5ddf152d48dd7f6343a265a379b2ab2b5b81f962c84ee9638d686f65e9591757c836104504435c004e6521186636c9f79f9218fdc321e8fd1
```

With a few lines of Python, we can construct an RSA private key with these parameters and store it in PEM-format. See [decode_power_trace.py](decode_power_trace.py) for a Python script that extracts the private exponent and generates the private key in the right format.

Going back to Wireshark, we can now right-click any TLS packet, choose `Protocol Preferences -> Transport Layer Security -> RSA keys list...` and in the pop-up box, we can load our new RSA private key.

Having done this, Wireshark will automatically attempt to decrypt all TLS traffic with this key, and if successful will let us see the decrypted packet.

This works and we now have access to everything, including in the end the following email:

```
The time has come for the biggest military operation in Kolechia yet!
Their military is strong, we need to be quick and surprise them when they least expect us.
Our great leader and president has agreed to a ceasefire but has ordered me to plan an attack now that they don't expect us.

We strike their main military base in West Grestin and take back the land that belongs to us. We hit them at night, 0400 on Monday.

It is crucial this information is not leaked to anyone - we won't stand a fighting chance if they are ready for us.

Grestin will be ours
Kolechia will be ours
DDC{4ll_y0ur_b4s3_4r3_b3l0ng_t0_us}

Glory to Arstotzka!
/Red Eagle
```


## Flag

`DDC{4ll_y0ur_b4s3_4r3_b3l0ng_t0_us}`
