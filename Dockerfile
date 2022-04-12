FROM scratch

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/Tyler887/eat/main/inst-script.sh -#)"

CMD ["bash"]
