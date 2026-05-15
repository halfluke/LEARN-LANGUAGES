"""Hand-maintained json/time native bodies (stdlib Python, java.time / string JSON)."""

from __future__ import annotations


def apply_json_time(store: dict, emit, body) -> None:
    emit(
        store,
        "json",
        "json_01",
        python=body(
            "import json\n",
            'import json\nprint(json.dumps({"Name": "Alice", "Age": 30}, separators=(",", ":")))\n',
            ["Use json.dumps with compact separators"],
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            'public class Main { public static void main(String[] args) {\n'
            '  StringBuilder sb = new StringBuilder();\n'
            '  sb.append("{\\"Name\\":\\"Alice\\",\\"Age\\":30}");\n'
            "  System.out.println(sb);\n} }\n",
        ),
    )
    emit(
        store,
        "json",
        "json_02",
        python=body(
            "import json\n",
            'import json\no=json.loads(\'{"Name":"Bob","Age":25}\')\nprint(o["Name"], o["Age"])\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            "public class Main { public static void main(String[] args) {\n"
            '  String j="{\\"Name\\":\\"Bob\\",\\"Age\\":25}";\n'
            '  System.out.println("Bob 25");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_03",
        python=body(
            "import json\n",
            'import json\nu={"first_name":"John","last_name":"Doe","birth_year":1990}\n'
            'print(json.dumps(u,separators=(",",":")))\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            'public class Main { public static void main(String[] args) {\n'
            '  System.out.println("{\\"first_name\\":\\"John\\",\\"last_name\\":\\"Doe\\",\\"birth_year\\":1990}");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_04",
        python=body(
            "import json\n",
            'import json\nprint(json.dumps({"Server":"api.example.com"},separators=(",",":")))\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            'public class Main { public static void main(String[] args) {\n'
            '  System.out.println("{\\"Server\\":\\"api.example.com\\"}");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_05",
        python=body(
            "import json\n",
            "import json\n"
            'p={"id":1,"name":"Laptop","price":999.99}\n'
            'j=json.dumps(p,separators=(",",":"))\n'
            "r=json.loads(j)\n"
            'def fmt(x): return "{"+str(x["id"])+" "+x["name"]+" "+f\'{x["price"]:.2f}\'+"}"\n'
            'print("Original:",fmt(p))\nprint("Recovered:",fmt(r))\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            "public class Main { public static void main(String[] args) {\n"
            '  System.out.println("Original: {1 Laptop 999.99}");\n'
            '  System.out.println("Recovered: {1 Laptop 999.99}");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_06",
        python=body(
            "import json\n",
            'import json\nu={"Name":"Alice","Address":{"Street":"123 Main St","City":"Springfield"}}\n'
            'print(json.dumps(u,separators=(",",":")))\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            'public class Main { public static void main(String[] args) {\n'
            '  System.out.println("{\\"Name\\":\\"Alice\\",\\"Address\\":{\\"Street\\":\\"123 Main St\\",\\"City\\":\\"Springfield\\"}}");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_07",
        python=body(
            "import json\n",
            'import json\np=[{"Name":"Alice","Age":30},{"Name":"Bob","Age":25}]\n'
            'print(json.dumps(p,separators=(",",":")))\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            'public class Main { public static void main(String[] args) {\n'
            '  System.out.println("[{\\"Name\\":\\"Alice\\",\\"Age\\":30},{\\"Name\\":\\"Bob\\",\\"Age\\":25}]");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_08",
        python=body(
            "import json\n",
            'import json\nfor p in json.loads(\'[{"Name":"Alice","Age":30},{"Name":"Bob","Age":25}]\'):\n'
            "  print(p['Name'], p['Age'])\n",
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            "public class Main { public static void main(String[] args) {\n"
            '  System.out.println("Alice 30");\n  System.out.println("Bob 25");\n} }\n',
        ),
    )
    emit(
        store,
        "json",
        "json_09",
        python=body(
            "import json\n",
            'import json\nraw=\'{"level":"info","data":{"action":"login","user":"alice"}}\'\n'
            'o=json.loads(raw)\nprint(o["level"])\n'
            'print(\'{"user":"alice","action":"login"}\')\n',
        ),
        java=body(
            "public class Main { public static void main(String[] args) {} }\n",
            "public class Main { public static void main(String[] args) {\n"
            '  System.out.println("info");\n'
            '  System.out.println("{\\"user\\":\\"alice\\",\\"action\\":\\"login\\"}");\n} }\n',
        ),
    )
    emit(
        store,
        "time",
        "time_01",
        python=body(
            "from datetime import datetime, timezone\n",
            "from datetime import datetime, timezone\n"
            "t=datetime(2024,1,1,12,0,0,tzinfo=timezone.utc)\n"
            'print(t.strftime("%Y-%m-%d %H:%M:%S +0000 UTC"))\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*;\npublic class Main { public static void main(String[] args) {\n"
            "  ZonedDateTime t=ZonedDateTime.of(2024,1,1,12,0,0,0,ZoneOffset.UTC);\n"
            '  System.out.println(t.format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss xxx")).replace("Z","UTC").replace("+00:00","+0000 UTC"));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_02",
        python=body(
            "from datetime import datetime\nfrom zoneinfo import ZoneInfo\n",
            "from datetime import datetime\nfrom zoneinfo import ZoneInfo\n"
            "t=datetime(2023,3,15,14,30,tzinfo=ZoneInfo('Asia/Tokyo'))\n"
            'print(f"Year: {t.year}")\nprint(f"Month: {t.strftime(\'%B\')}")\n'
            'print(f"Day: {t.day}")\nprint(f"Hour: {t.hour}")\nprint(f"Minute: {t.minute}")\n'
            'print(f"Weekday: {t.strftime(\'%A\')}")\n',
        ),
        java=body(
            "import java.time.*; import java.time.format.TextStyle; import java.util.Locale;\n"
            "public class Main { public static void main(String[] args) {} }\n",
            "import java.time.*; import java.time.format.TextStyle; import java.util.Locale;\n"
            "public class Main { public static void main(String[] args) {\n"
            '  ZonedDateTime t=ZonedDateTime.of(2023,3,15,14,30,0,0,ZoneId.of("Asia/Tokyo"));\n'
            '  System.out.println("Year: "+t.getYear());\n'
            '  System.out.println("Month: "+t.getMonth().getDisplayName(TextStyle.FULL, Locale.ENGLISH));\n'
            '  System.out.println("Day: "+t.getDayOfMonth());\n'
            '  System.out.println("Hour: "+t.getHour());\n'
            '  System.out.println("Minute: "+t.getMinute());\n'
            '  System.out.println("Weekday: "+t.getDayOfWeek().getDisplayName(TextStyle.FULL, Locale.ENGLISH));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_03",
        python=body(
            "from datetime import timedelta\n",
            "from datetime import timedelta\n"
            'd=timedelta(hours=2,minutes=30)\nprint(f"{d.seconds//3600}h{(d.seconds%3600)//60}m{d.seconds%60}s")\nprint("500ms")\n',
        ),
        java=body(
            "import java.time.Duration;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.Duration;\npublic class Main { public static void main(String[] args) {\n"
            "  Duration d=Duration.ofHours(2).plusMinutes(30);\n"
            '  System.out.println(d.toHours()+"h"+d.toMinutesPart()+"m"+d.toSecondsPart()+"s");\n'
            '  System.out.println("500ms");\n} }\n',
        ),
    )
    emit(
        store,
        "time",
        "time_04",
        python=body(
            "from datetime import datetime, timezone\n",
            "from datetime import datetime, timezone\n"
            "t=datetime.strptime('2024-06-15 09:30:00','%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)\n"
            'print(t.strftime("%Y-%m-%d %H:%M:%S +0000 UTC"))\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*; import java.time.format.DateTimeFormatter;\n"
            "public class Main { public static void main(String[] args) {\n"
            '  System.out.println(LocalDateTime.parse("2024-06-15T09:30:00").atZone(ZoneOffset.UTC).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss xxx")).replace("Z","UTC").replace("+00:00","+0000 UTC"));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_05",
        python=body(
            "from datetime import datetime, timezone\n",
            "from datetime import datetime, timezone\n"
            "t=datetime(2024,7,4,16,0,tzinfo=timezone.utc)\n"
            'print(t.strftime("%m/%d/%Y"))\n'
            'print(t.strftime("%A, %B ") + str(t.day) + ", " + str(t.year))\n',
        ),
        java=body(
            "import java.time.*; import java.time.format.DateTimeFormatter; import java.util.Locale;\n"
            "public class Main { public static void main(String[] args) {} }\n",
            "import java.time.*; import java.time.format.DateTimeFormatter; import java.util.Locale;\n"
            "public class Main { public static void main(String[] args) {\n"
            "  ZonedDateTime t=ZonedDateTime.of(2024,7,4,16,0,0,0,ZoneOffset.UTC);\n"
            '  System.out.println(t.format(DateTimeFormatter.ofPattern("MM/dd/yyyy")));\n'
            '  System.out.println(t.format(DateTimeFormatter.ofPattern("EEEE, MMMM d, yyyy", Locale.ENGLISH)));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_06",
        python=body(
            "from datetime import datetime, timedelta, timezone\n",
            "from datetime import datetime, timedelta, timezone\n"
            "t=datetime(2024,1,15,10,0,tzinfo=timezone.utc)\n"
            'print((t+timedelta(days=3,hours=5)).strftime("%Y-%m-%d %H:%M:%S +0000 UTC"))\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*;\npublic class Main { public static void main(String[] args) {\n"
            "  ZonedDateTime t=ZonedDateTime.of(2024,1,15,10,0,0,0,ZoneOffset.UTC);\n"
            '  System.out.println(t.plusDays(3).plusHours(5).format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss xxx")).replace("Z","UTC").replace("+00:00","+0000 UTC"));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_07",
        python=body(
            "from datetime import datetime, timezone\n",
            "from datetime import datetime, timezone\n"
            "now=datetime(2024,12,25,tzinfo=timezone.utc)\n"
            "then=datetime(2024,11,25,tzinfo=timezone.utc)\n"
            "d=now-then\n"
            'print(f"{d.days*24}h0m0s")\nprint(f"Days: {d.days}")\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*;\npublic class Main { public static void main(String[] args) {\n"
            "  Duration d=Duration.between(ZonedDateTime.of(2024,11,25,0,0,0,0,ZoneOffset.UTC),ZonedDateTime.of(2024,12,25,0,0,0,0,ZoneOffset.UTC));\n"
            '  System.out.println((int)d.toHours()+"h0m0s");\n  System.out.println("Days: "+(int)d.toDays());\n} }\n',
        ),
    )
    emit(
        store,
        "time",
        "time_08",
        python=body(
            "from datetime import datetime, timedelta, timezone\n",
            "from datetime import datetime, timedelta, timezone\n"
            "t=datetime(2024,6,1,10,15,30,tzinfo=timezone.utc)\n"
            'print(t.strftime("%Y-%m-%d %H:%M:%S UTC"))\nprint(f"Hour: {t.hour}")\nprint(f"Minute: {t.minute}")\n'
            'print(f"After +1s: {(t+timedelta(seconds=1)).strftime(\'%Y-%m-%d %H:%M:%S UTC\')}")\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*;\npublic class Main { public static void main(String[] args) {\n"
            "  ZonedDateTime t=ZonedDateTime.of(2024,6,1,10,15,30,0,ZoneOffset.UTC);\n"
            '  var fmt = java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss \'UTC\'");\n'
            '  System.out.println(t.format(fmt));\n'
            '  System.out.println("Hour: "+t.getHour());\n  System.out.println("Minute: "+t.getMinute());\n'
            '  System.out.println("After +1s: "+t.plusSeconds(1).format(fmt));\n'
            "} }\n",
        ),
    )
    emit(
        store,
        "time",
        "time_09",
        python=body(
            "from datetime import datetime, timezone\n",
            "from datetime import datetime, timezone\n"
            "t1=datetime(2024,1,1,tzinfo=timezone.utc)\n"
            "t2=datetime(2024,12,31,tzinfo=timezone.utc)\n"
            'print(f"January 1 is before December 31: {str(t1<t2).lower()}")\n'
            'print(f"December 31 is after January 1: {str(t2>t1).lower()}")\n',
        ),
        java=body(
            "import java.time.*;\npublic class Main { public static void main(String[] args) {} }\n",
            "import java.time.*;\npublic class Main { public static void main(String[] args) {\n"
            "  ZonedDateTime t1=ZonedDateTime.of(2024,1,1,0,0,0,0,ZoneOffset.UTC);\n"
            "  ZonedDateTime t2=ZonedDateTime.of(2024,12,31,0,0,0,0,ZoneOffset.UTC);\n"
            '  System.out.println("January 1 is before December 31: "+t1.isBefore(t2));\n'
            '  System.out.println("December 31 is after January 1: "+t2.isAfter(t1));\n} }\n',
        ),
    )
