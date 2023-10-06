main:
	python3 python/main.py AAMAS2015 0.00
	python3 python/main.py ICLR2018 0.02

parameter:
	python3 python/parameter.py AAMAS2015 0.00
	python3 python/parameter.py ICLR2018 0.02

hypertune:
	python3 python/hypertune.py AAMAS2015 0.8046875 0.04
	python3 python/hypertune.py ICLR2018 0.8984375 0.02

additional:
	python3 python/main.py Preflib1 0.00
	python3 python/main.py Preflib2 0.00
	python3 python/main.py Preflib3 0.00
	python3 python/main.py AAMAS2016 0.00

speedcpp:
	g++ cpp/speed.cpp -o speed -O3
	time ./speed AAMAS2015 PM-Q 0.8046875 0.1181640625 0.25390625 0.0
	time ./speed AAMAS2015 PM-E 0.8046875 0.1181640625 0.25390625 0.0
	time ./speed ICLR2018 PM-Q 0.8984375 0.2119140625 0.5078125 0.02
	time ./speed ICLR2018 PM-E 0.8984375 0.2119140625 0.5078125 0.02
	rm speed

speedpython:
	time python3 python/speed.py AAMAS2015 PLRA 0.8046875 0.1181640625 0.25390625 0.0
	time python3 python/speed.py AAMAS2015 PM-Q 0.8046875 0.1181640625 0.25390625 0.0
	time python3 python/speed.py AAMAS2015 PM-E 0.8046875 0.1181640625 0.25390625 0.0
	time python3 python/speed.py ICLR2018 PLRA 0.8984375 0.2119140625 0.5078125 0.02
	time python3 python/speed.py ICLR2018 PM-Q 0.8984375 0.2119140625 0.5078125 0.02
	time python3 python/speed.py ICLR2018 PM-E 0.8984375 0.2119140625 0.5078125 0.02

plots: 
	python3 plot/main.py Preflib1
	python3 plot/main.py Preflib2
	python3 plot/main.py Preflib3
	python3 plot/main.py AAMAS2015
	python3 plot/main.py AAMAS2016
	python3 plot/main.py ICLR2018
	python3 plot/hypertune.py AAMAS2015 0.04
	python3 plot/hypertune.py ICLR2018 0.02

clean:
	rm *.jpg -f
	rm *.log -f