README.html : test/README.md ./test/render_file.py
	python ./test/render_file.py test/README.md

.PHONY : clean
clean :
	del /S test\*.html