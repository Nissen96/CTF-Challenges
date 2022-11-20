ct = "lafeT hgDCDs  i{1tp1Spwyp1pw_4str_uyy0_p3xt1ln4t0wns__1_0pr_mpy3 C.yr}toultrnaga!2sotni2"

known_pt_block = "The flag"
perm = [ct[:8].find(c) for c in known_pt_block]

message = ""
for i in range(0, len(ct), 8):
   for j in perm:
      message += ct[i + j]

pad = int(message[-1])
print(message[:-pad])
