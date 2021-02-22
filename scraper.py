from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re

URL = "https://virtuale.unibo.it/course/index.php?categoryid=12&browse=courses&perpage=20&page=0"
LOGIN = "https://idp.unibo.it/adfs/ls/?SAMLRequest=fZHNTsMwEIRfJfK9sZ3%2BUauJFNoDlQpETeDABdmJSyw5dvA6Bd6etAG1HOh5Z7%2BZnV0Cb3TL0s7XZiffOwk%2B%2BGy0AXYaxKhzhlkOCpjhjQTmS5an91sWhYS1znpbWo2CFEA6r6xZWQNdI10u3UGV8mm3jVHtfQsM44NyvuNahp1RwobK47xWQlgtfR0CWHwERzh7zAsUrPskyvAj80xQVXte5tUesAaMgs06Rq9TPp8s%2BLSc31SzPSFiMqN0LBaUE0m4kKSXAXRyY8Bz42MUkYiOSDSipKCUjSkj0xcUZD8n3SpTKfN2%2FX4xiIDdFUU2GnI%2FSwenzL0AJctji%2Bxk7C56vY7lv2Wi5N%2FqlviCPNi07KFHbdaZ1ar8ClKt7cfKSe5ljCjCybDy99fJNw%3D%3D&RelayState=https%3A%2F%2Fvirtuale.unibo.it%2Fauth%2Fshibboleth%2Findex.php&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=eKYi8JlsOdhxMAdaQ0qOxS%2B8PSzYIQvtJvji43qJ%2B8tTR0DC7OVOsBsSKd7yPy%2Bvrq%2FmguHRygc43YC5reD8ht74M8v5TbAF4GYW%2BznL6ZiLt7yXgMfEt%2Bu3HHnJHHLU1hCY7bm1E0j7VnEgOpE5gvPT8RlU3HUyjbkmOXTxnAGwGFvoy1fvBAsT%2B3WpmO4YjDMKEZMqNUXVkTU3SXCMy3LdT1TwSf47WqJPGcc%2B8m%2B1wV6YlXYxB0XqtiAczpbbBsaTcdk5eFwXviTpdBD%2BAN7gS%2F%2BIcThEn%2BAKX64ln6Okb2jr62YJCnXFBZTnsQC%2F6WVXb7RQ4srJoVPD3GA8sTM6eX811ILkzD6BhXeGIbPjcKlymVehBGtxcTlu%2FT8cHdl9k%2BqfGC9t1IBjiIU%2FB8Sb%2BWDsetNdp6PQ3E6TCIrujyCDH2PSi1Wks3eVkkP6l83t1MlyYSEMahZ0jRusXYivA6W71U2GoOJobgxqzpdqja5EBmFTNmWfeJ%2B%2B83RM&client-request-id=b7ef3bef-335e-4daa-9200-00800100009a"
HIDDEN = "https://virtuale.unibo.it:443/Shibboleth.sso/SAML2/POST"
with open("login.json") as f:
	login = json.load(f)
payload = {"UserName": login["user"],
		   "Password": login["password"],
		   "SAMLResponse": "PHNhbWxwOlJlc3BvbnNlIElEPSJfNzFjZjYzNDYtYTBiOC00YmE3LWIxZGEtNGZkZjkyMzY3MTllIiBWZXJzaW9uPSIyLjAiIElzc3VlSW5zdGFudD0iMjAyMS0wMi0xMVQxNzoxNToyMC44MjJaIiBEZXN0aW5hdGlvbj0iaHR0cHM6Ly92aXJ0dWFsZS51bmliby5pdC9TaGliYm9sZXRoLnNzby9TQU1MMi9QT1NUIiBDb25zZW50PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6Y29uc2VudDp1bnNwZWNpZmllZCIgSW5SZXNwb25zZVRvPSJfZjg5YzMzMjYzYjM5OGM5YjY3Y2MzYzI1N2FlZmM4NzEiIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiPjxJc3N1ZXIgeG1sbnM9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iPmh0dHA6Ly9pZHAudW5pYm8uaXQvYWRmcy9zZXJ2aWNlcy90cnVzdDwvSXNzdWVyPjxzYW1scDpTdGF0dXM%2BPHNhbWxwOlN0YXR1c0NvZGUgVmFsdWU9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpzdGF0dXM6U3VjY2VzcyIgLz48L3NhbWxwOlN0YXR1cz48RW5jcnlwdGVkQXNzZXJ0aW9uIHhtbG5zPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj48eGVuYzpFbmNyeXB0ZWREYXRhIFR5cGU9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI0VsZW1lbnQiIHhtbG5zOnhlbmM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jIyI%2BPHhlbmM6RW5jcnlwdGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI2FlczI1Ni1jYmMiIC8%2BPEtleUluZm8geG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyMiPjxlOkVuY3J5cHRlZEtleSB4bWxuczplPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGVuYyMiPjxlOkVuY3J5cHRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGVuYyNyc2Etb2FlcC1tZ2YxcCI%2BPERpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNzaGExIiAvPjwvZTpFbmNyeXB0aW9uTWV0aG9kPjxLZXlJbmZvPjxkczpYNTA5RGF0YSB4bWxuczpkcz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI%2BPGRzOlg1MDlJc3N1ZXJTZXJpYWw%2BPGRzOlg1MDlJc3N1ZXJOYW1lPkNOPWxhenAtbW10aWQyMC0wMS5wZXJzb25hbGUuZGlyLnVuaWJvLml0PC9kczpYNTA5SXNzdWVyTmFtZT48ZHM6WDUwOVNlcmlhbE51bWJlcj40NTQxNTE4NDQyNzE5MDY2NTQyNzA1OTQ5NDg5OTQzNTkyMjU0NjExNDI5MDQ4NzM8L2RzOlg1MDlTZXJpYWxOdW1iZXI%2BPC9kczpYNTA5SXNzdWVyU2VyaWFsPjwvZHM6WDUwOURhdGE%2BPC9LZXlJbmZvPjxlOkNpcGhlckRhdGE%2BPGU6Q2lwaGVyVmFsdWU%2BVkYwdFZyS1YyVVpTMUpxbldvUW5CVHZkNHZ4NEtlZWlzVnN2S3NCQitVVDlDVEVZa0s1UGFvS3cwT2VOeENFNHJjZjJ0V0ZpR0xxVmR0M3ZwWko1NjFTa0FnZ1hWbTFaZmVPS1pwM3hPTEoxTzBackN5NmR4aHhlcFVGMUFicmkwdGREWXphTFNlWSsxU01mUFpaeld6TGs1eVFyQWpsL3JOYm54UlEvd0t5MXB1R0tBM2FUSmg2cngwaWNuVE9TRFUwSzU3WENhYktiYVhxWE9oMzlHMEVReGZ6SVMvSjdEUEZvRkh1Zzgva29iN21oWC9NU1pDWUFQanoxbDNXVDhWSFdlQTRCVDI4NkRtRUtjbEY5eDQvVmZNQU9kYXJUbEZqYzFpQ0xYV0s0aE1Jc2dwd3hnektIblpmMGZORHVNaXBxcWtjcUErK2tWVTBSc1BwMmJzdFRNaGUvamR3aXAySnZpTFpzaGtVdHJMYlBnUTM2aklwSzU3N0tGdDZncUp4VXArWmxseDJyVU51V1EwUTR1NWNPck1xWGt2eVhJNUZtWEJNWTZ1ODdtSmorWXB4RjIwK1lqVG00b1FMVktXOEEzWjB2T1N4aFBLc3FKRGVtNUdpTld4N2tOdXNheXVuaC9XazM5QTArN08yOXBab0Y3S0xXK3pUbFo5MTg8L2U6Q2lwaGVyVmFsdWU%2BPC9lOkNpcGhlckRhdGE%2BPC9lOkVuY3J5cHRlZEtleT48L0tleUluZm8%2BPHhlbmM6Q2lwaGVyRGF0YT48eGVuYzpDaXBoZXJWYWx1ZT4xdzZGTTlQYUUzZjNxTjRhTzlLa2FESXFHOGVEdjluaEVLOFJXLzZCMGV5MUowUkhGMUhLYmFMZDRwWVBLV3pFUGlFVU5BQlRNRDdvajdRUmphMlpXYTc3SnRaQ21BUVNUcUR3eElLMzJsdjl3S1pzU3lqcjV6bXM0RmNCSWR5U29HWWdDQUwySWhNa3UzdjlyQ09FUW5GMXdoN2JpdnpUbm5XWW5oempIK1pORFp2OUY2eTVEZnF3dHowbjNYNFR6VFlZTGl1Q3Zzc2h0SExGSi9PSEF2dFlVZFJzcW1pTitxczJQdHdRSkdHVHJYODFYcDJ2YmZTaGVWSUNlYlJwbVkxbm0xQlpVRjNZVjFrZDdpem1iYnRleDlQV2VTMnRQM1ZxaFhEZDVWMU81RzJPaXRiempPUnMxZGNYY3d1cXlOdDcwenFxSE9VK3ZIMGVxc2dHMGFGejdFdDhoQTVtTnZaMUZyT1ZjdmY5T3ZwMUdXb1M0ZkZYZVlLUnMwSkQ1Z3dMRTVlcngwWUZCUmtPcllrOTF4Ukw4cDZLMDloYzlsUVY1RkxSYys3cEFwdytlbWt3WXRBMzhPSTNkblo4bXpmcEJIQ3dCenR5Y1JDQ3ZDc09qR0wzTGZIZmd0M1J3WWFJS1ZwQytJMzUvN2VBbTRxUVh3ZGJSd1oyeTBHeHNpVWhkNnNPaTU0cjFCWDdnNUlaQm43aHlKdzhMSEJsZkw4OXlBTU1MK0pSZExYRTRRU0VRblBkVjYrNk44dVVSUjFwNUJGNE9aTU9IbEcrVFVBZHRHbWloTWVFQ1NCZnNQcGZwOWNXNWNZWDM0a3gwOEJUb3N1Z1FMTU95ZjNkNGlxZ3BWVHR2N2swKzBCSldtZFZVNkQ1eE5kdGJwUFgxQmpHaERYUjdsOEoxZE05a2dmejlzUVJhZzI0b0JzSjNvL0xlNU5uU29mb1kzanpobEo1dHpGRE5tVGlQd3RYcHM5emV3VUk2bzRweExkSEdkeUVKcjZ5NlpaS1NyWjFibVh1dFIwNi9NZmx6ZVN1WTJ6M2ljTXFiMXN6NEd3Y2psbDdIeHlYZUZEbE01a0FPSmc3T2VYYlRrZEx2RWx6a05GNjFNcjhVRDkvaEdld2V3SllQcTNabmE5dHJlT1ZsdTJjVTlIMEEraU9lRi9wOUlxWm9IWktHZU44YnpvRUxjV0U5SjhwTHRrd2pmeDdGbG51UGxnNDZhSUJSYTdXSVZVb0RwdkhmQ2RHdnR0b2MyOXVqd1FDUFZ2UG02YWNNSTQzT2dRdDVoQ2xONTZ4eVJxREhNSXBBSUNyRE5NNExjSU5nekpaMnIzQ2VLR0VyZEZvemVJM0RSaGg0czEyYjhQajZWTzdQV2lFcHNIdUcvVXpTNFJYOW5aTldaekJzeFFYMVFRdmNmeVNXRXZoU0JmTk9RZVFCbDkrWHZtWFpUNzBlektSUzc1S3JrRGIwMkkza0wxNnQ4b1h4blhyRlMxWDZNaDBBbzY2cmt6cXBoblptNGIwaGdTcFZ4eWI1NC9pL2lxRlQ5UTkwS3FoYXVZSUxNWngzdmJHSVIvY0tqaHg4dlFBOFp4Rm4rNlBoaThza3V3TzdyektoamlqbitZZHFCNGZUSTU5TXdWQkU3QWJTYWJRQjBIMFdTVXpxN200cXk0REVkOFJwcXpIanVXNzN0aGNvNHVxSXBCTzM5aGl4emV1T3g5ZXo2ajc2UkUySXZZeHo0QjFVcTF5YmdlanR3MytQc2RWUFhGdGNUSVJkdkp6cmFvNnBYbW9WNFpCT2hkK3RlYWhmUm9EeWc5RkwxRDJ5VVpuUFBRdU9yN2EveHh6N1EvclE5M3RCSFVhajUwY2h1aXV3OW1XdS9tU3ZjeFVHNEtuSkpWbjBRbkgwL2Izdk5yV25odHBSQVJNWjRIdSs4blliN1lEbXJPUXRTOEg4VFNQRDJZUTdrVk5YRUUybkRIZjVwQUMyeC84T0FCTm1qaTZPZU5VdkdZdGJ5L2FjclNOVzRMbllZc1dqYXFQaXZtRi8xR2RnRnI0d1BaM0JoQnU2NEtxdGdvSTlweVRjRWp1Smc3MzVUTmc3NDJHL3BWS2ZoaWNBMEwwNnl5dU55RUdCVUVwV0ZhNmVwL3VlbUJBNDZ1Z2VJMmpVUU9hMEFkZm0ra0t3aVJpbXNaRW56aG95OStnSGRIZ0NxTytOTmJIcDNqSTJ5eWM2K3h3eW1rZHp1dllneXRLOXV0YlFaTmw3eG1KcXR4U29MWlpPbEFjQmRqWUowS1R2Q1FGbGJEaDk2MnE4Mm1Ba2hnWTRteFdVd1piV04xQ1d5M3A4ZXBEQ2xZVFM1NE1TZUZuNFJVb3R6cjBMakNkR0VIWmtZK3lmenAxbnd0SGFnbHRyRkZwVElTajNwaXplSjJCclUzYTlmMUV6d3dsYWdZVG5wcXhzNElud3dSWVUvazkyMk5UV3pDL25aa2NsRGhpWUh3YVZLOENzdml2b2pWdEtTWEpJUXJTZk56Y3U2azNJTjRxNzQrN25OeGF0YkNrb1BzRk9lQ3VnQXErcTdJVEkvbWhCbFF4akUxK0wwVC94N2l6WS80OUJFSkgvbytNVjZUbk91L1JqSXFzcVVkLy9FbUhZa2dvOW9tbGdqYXZFUHE0R2pNSEdwaGdaOURveHN0OUpjN1hKZGRkbkMrNy9CSmlJOVo0U2YzNFhzUVp1N2VoRGhTZXUrbS9YZWxpMGZuRUl6bDdFRDF2d2M5Nm5qVElabkFnRWZrM3Z0ZVZaL1BnNEZTZDJvNzFaWG5SMjhXUTZhWThmZk8wYkUxeTJwZVR5OUZEeEQ1V2ptdVRlcHFkR24rOXpwazc4Zk5hdlZrZW1tQTRoazlNbGlrcDBsVWR5dGIvNnpGY2xERFNWdVlVUXcrNUEzK0EzZ0x5d3ZDWFc4bGRhREV3VE5OSFJPcG5uODNVOXBwTlRtTEJiWTk3enNJVVV1ay95b3NWTWJzUGRlNzNDVkhiWHpBUHp6ckFqdXNKWDViVFVYc3Mxa3R5VnQzeVVPV0ZnQThzcStRQS9UNjNNc1lXZ3llZmYwUWNWc21neURWUytUbmRhKzNUeWlrNGg4ck1wUWJ1a1l5L1VJWFpqZzhpOGZkUGpnQjJ3a3Q3ampqNHFnR3grZlBHbi93VTlMdEI4bFRxUzFhdTlZeEIxK0FNcWhlVWNxVGdxeW83M2RYUDdEV1pjeVJOM3FaUFk0STF0R3hJVGRLV0dqUTFUTEZMdjBUcnhyK2RRVG0rT29lU1RoNnFzRVZidEVDOHNHaTF3RzlUQnNFS21QeUNvTHVINkRqWkY3V3RFTjVnVG5tUjlzSmt1TCt4QlhlaFlOOUJ1WVlvbkdmU05QUGdXQXdiZlltMEpmdUcxUDA4SkxFSEIrc3VnZkthcVBpUGhMdXVrSm1aN2MwM2huNTV0S0RhMXJCSVhrL1VCVmRCeXRuOVpxcE5qRkJpQjQ4MVl0TFR2Z2xxejlQNWRROEhFQTk1cnFtYkxER2F1MEZGUDFFZDJvdDlKRnA1anNnamxNR2JMb3RKU0VKdmNsa3AxREM2d3ZSTXFNQUtuOWNEMHpOeDlIZHZOWE5DcmFmWlRaQ3RwSGwzcjJvK0FUak5WM0t1akVGVjdoQkFvbXRnNUd1dXFwa2dPdWE5dTNsS3JHSGtocm4rUDY3WHVORGtXTmRVMTJwNXBiQ1JucjFIdFFXZlF2VnlyRlZGdDgxQ1prZDNSWmRjTXVwSFpZZW9IL3F0aFhYSVE0cGkvZVRCcXNIbHlMYTV2MCtidndQN29qQzVuWDZZNWpqSTMybnpNME9jSlU0cUxDR0E2QTBUbzdoenpIOUpybCt0MGc0aXhIWTZpYms5Rm9LOC9mMVZZRVJkR2hBdFN6Mnh6bkN3bmJoQ1J5M2VjdWo3dEp1eTBNbmt1dVFNenpzdExqeGhjMXFnZkNCVWdSZXZVb3hQZXplSjgwaEdVZmM3V3RjQzN2bWRpanJJTnpjRUNIYXlxL2JIQVZ1NlR2MnE3QkpZUEJRUUpqWFNuMGF4Y210SitWYk1hbTlMdFR2UkR3VzNFcU16TEVHRWVVQmdXTWNVYlFLNWp3YW5DUGh4SVJES09GVzROZnFFUXZSM1VQSHZBd013VUQvQi9jZ1JtM1FsUkpaVTkwQkRBalRFY2ZZbEtCMTJORFl2VFlZYm5UOC9oMms2UEc2eWRNVXlCalBWajdQUnEyc1VRcUlJRzU0em9BdUJTRk53bW1WQkk5UnVHQ0ZxOW1HR0J3eEdTdXY5Qk5Rbm1VcFV3Mk5sSU4rdkUwTDN2R0VoWWcrRzFLL2IwQmlDdU1OamtYdEEyajkrRlRZVkcvSzRWc1hKZFV4OEhBU0s5T1AwaStIbzBERi8vMlhDdnh0Y283K3A5SVNROUtWRWlxMm9ZNlNUL21Ob0ZYZ2J4TnN0a2YzNStuOXhoYXlHVHlubk40OThHVC8yUWt6QlV1T0RqWU1FbmdVUzl0b2tvK3ZxQTdhakRpTGw4UXFNRE9qdnJxcm1YZVlDajlPUm8yVGp5OHBwdUI5bFdLeDIvYVBuSWF4aGRITEQ5SXNnTzNZbzB0R0psRUV0ZnlNWGx2RWVRQTdDS242dURPMkZZTkN3VkVTSDBqNmhPM3NkUHZhZi8xWjlzSjFGRFkwejRrbWRPQWdqTnl4KzhuVVczbHpqbVVRY2lPY1o5YkRQeTFLbVB6TDhha09EdVRISXFERHhVcU13MUNZWVVQVTFsVnRWR3JtbmN1VWcrWmE1b25xa3RJcW5pa3JRQy91T1JHaW12V05ENWJ3TVY4enV0YWZEdUN3azNtN1drOEo4bDVHb0IvNVIxdHV1bktjRkpmQ2RhYmJZeHJIUUxQQXhpM1FLUXd4eDJWbEVrRXJybkUxcjFrdzZIMVRNYjhUL2d1QWJ1TWdiSnlxTzV6TStOZ1pOeSthM29Kd2RqNFV1UERGSDVEMGsvQ28ydG0wamxmVTI0eGpnengyZVdWMDIwVmg0Nno5dEF3akpTalNBT0lMWk1vREdHalJzWTduVVhMMFpMcWQralltWU9vVytiT3YzSlJRTnJGemphQnFvektiY3IwZVNoaUR2c255NkdYN0YzQ3dpLys0TEo1cWh0UlZBOEdzVmtGWVdnVlBQQmpFTlNSNXk4Mmp5TnVhWWg1ZlJ6VU9aT3Rnc3pLMzc4ckRPWERteFhTM3FzQXdoQWQ2TDAram1zQ0Z6QlFKSlF2cWNtOEVlaUJDREtpRWdOMi9ORk1CTVljVE1MWCszYzVjRXVPdmcycGh2MmQ3MmdMYWRubGg3T0hzVW9wQkVBamhOZXlKa2hzUFVQRzhydTR2T3FldlFhbHBHbXB6L1lyNlV5VDJTRE54aUJ5NWFEVTlkb0t4YlNIYjJDZS9ZZVlGT0JrQzBNRGxYWVJhMEp3SkxtRHFXUnRZMjZkNHRvL2ZpRGRidW8rcXlUNW9CNG05OERaWXJTREVBL1phNGMzUHl2dDZrc05kN0ZtRGh1QllYd2YyVGh2SExTckFTWHlrNEQvWWVuZUlla095MWwyTVk4TWpxdXNNNnc5WE0yQ0hkUDRuNGViMC92S3RpcjdPbmFNcTUxOUU0S3BnZ2JXMnZ2MUl5OGVVcG11VFBiYWVDbVlvdmhCdXlHRTBoSHE4K1djelR0QzNlZjRaZldsY0pzRC8xdlRWUW1jWWRRdUR2SEQ5YTQ3R1k1c2lUcGJFVjJOT3lRWXQvbWVDM3JZZjJoVWtTdXp6ZWJqbndCRXM3d2pDRWk5UGVyMHFzTTRqZmJlTlBlQnZhZkMyOUlLeGp4anZ2cXRuZEVMNDMxTmEwY0ZtVWlNRnRoOE9HRzk4SHFidXI3blc1cFg0NEhwNGo4QmRrbzZxQXE1bXZ1NEpOL3J1b1R2RHh6OWUvZGN0bnZRUytYK2RmRkovSzUwQkdFeXdUZ0kzSGFFUnExTUF5NXZkVTRPWWlDUGt0VzZQNFVIK1ZGcmhvZWlNNjNaS0gzSUV5c1Y3TzNIZjVGdnlYL2l1R2ZjWUJiQStqb0Y5VjJHWnhJREJkT3JwYWM5Nkhkc2JNTTd4VXNudm5vVHlqak56eUxjb1dIWkdVVVhIYjZHMlV5dkViSFE4SU5adlRsVVZXRmZzcHNkaHFONmhFRVYya0lHNGFBQUJnN09mREdNV1F0azI5a1p2ZXdic2lXTnhydHEvY25DejBabm14dS9FVndOM0hkcFhLZG1vdFdiQnF4cGFjdlV3SlFuSi85b0c1NzFjYVRVZUE2VGNEb3A3Sll0M3hjc1lsbjJhZWpGcVNmM2sxd2h4ZGxQN0RyUno1K1kyaVk2ZzdsRUtlbGV4ZXpNclBYK3dCLzVwRGcvVXN5aTRhUGN4NWhlckhGa05YK2hGajhGZ3hNU1RFSG5Sc20rbEVqTis3VUF0Z01iQWY5T0Q3am0wQUpKZFdad0xxVjJDV2sxZkdWQUF5K0JxS3I2Ni9SVmYwS2kyTUJYeFd2eUIydUN1VVA4cWtXM1BadVZXZEQvVjdmTGpucVBpTWJQVUNsNkY5cnJXZnRHYmNkRlMxUWgzOVFLbUx5VllGZ2s3Q1VHU0ZNR3U4S1R6elc4ejBzSG9zNEd6RkJJU0N0YUxzb3FpOFgrOWRIWDFYMU41S3laZVVKNHNILzE5enkyb0d3dWlYd2pFWkVnTUF3YUgrOFZ5Z0JTOWRpMDBLZnB2Q0VyeWNtM1JWaG5GVGw0MWw3LzRLdFdmZVlDdzFUVHNZd0NQQ3Q1TUUrMlhFQ3JuMzZPeUI2RkdjU1FsR2hjN3B2U3Y5RFZ1aHQ3M3h0Tkw1QTBxUnpyNS9wOEFFajliM1VHczNIRFp1YkltcW1tVzU8L3hlbmM6Q2lwaGVyVmFsdWU%2BPC94ZW5jOkNpcGhlckRhdGE%2BPC94ZW5jOkVuY3J5cHRlZERhdGE%2BPC9FbmNyeXB0ZWRBc3NlcnRpb24%2BPC9zYW1scDpSZXNwb25zZT4%3D&RelayState=https%3A%2F%2Fvirtuale.unibo.it%2Fauth%2Fshibboleth%2Findex.php%3Ferrorcode%3D4"
}

with HTMLSession() as s:
	#logs in
	p = s.post(LOGIN, data=payload)

	#gets saml response from html
	soup = BeautifulSoup(p.content, "html.parser")
	value = ""
	try:
		value = soup.find("input", {"name": "SAMLResponse"}).get("value")
	except:
		pass
    
	r_payload = {"SAMLResponse": value}
	p = s.post(HIDDEN, data=r_payload)
    
	#gets links and names from courses

	data = []

	#if json exists, load it
	try:
		with open("20-21/courses20-21.json", "r") as j:
			data = json.load(j)
	#if json doesn't exist, generate it from html source
	except FileNotFoundError:
		with open("20-21/list.html", "r") as f:
			soup = BeautifulSoup(f.read(), "html.parser")

		courses = []
		try:
			list = soup.find_all("a", class_="aalink")
			for item in list:
				name = re.search(">(.+)<", str(item)).group()[1:-1]
				link = re.split("\"", str(item))[3]
				courses.append({"name": name, "link": link})
		except:
			pass

		with open("20-21/courses20-21.json", "w") as f:
			f.write(json.dumps(courses))

		data = courses

	#open course page and exclude closed ones
	php = "https://virtuale.unibo.it/enrol/index.php"

	#for item in data:
	item = data[1]

	page = s.get(item["link"])
	print(item["link"])
	soup = BeautifulSoup(page.content, "html.parser")

	r_id = soup.find("input", {"name": "id"}).get("value")
	r_in = soup.find("input", {"name": "instance"}).get("value")
	r_sk = soup.find("input", {"name": "sesskey"}).get("value")
	r_qf_k = re.search("_qf__(.+)form", str(soup)).group()
	print(r_qf_k)
	r_qf_v = soup.find("input", {"name": r_qf_k}).get("value")
	r_mf = soup.find("input", {"name": "mform_isexpanded_id_selfheader"}).get("value")

	#with open("20-21/page.html", "w") as f:
		#f.write(str(soup))
	payload = {"id": r_id,
				"instance": r_in,
				"sesskey": r_sk,
				r_qf_k: r_qf_v,
				"mform_isexpanded_id_selfheader": r_mf
	}

	p = s.post(php, data=payload)
	print(p)
	#enroll in a course
    