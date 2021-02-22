from .appIcons import Icons
import urllib.parse

def linkFile(kind,src):
    if(kind =="file"):
        htmlCode = """
        <div class="message sent">
            <div class="file">
                <div class="file-in">
                    <img src="{}" width="45" height="45">
                        <p>{}</p>
                </div>
            </div>
            <span class="metadata">
                <span class="time"></span><span class="tick"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg></span>
            </span>
        </div>"""
        fileName = src.split("/")[-1]
        shortFileName = fileName
        htmlCode = htmlCode.replace("\n","").replace("\r","")
        fileExtension = fileName.split(".")[-1]
        if(len(shortFileName) >= 19):
            shortFileName = shortFileName[:-1*(len(shortFileName)-18)]
            shortFileName += "..."
        if(fileExtension == "xlsx"):
            htmlCode = htmlCode.format("http://furkanyolal.com.tr/wpsend/icons/excel.png",shortFileName)
        elif(fileExtension == "doc" or fileExtension == "docx"):
            htmlCode = htmlCode.format("http://furkanyolal.com.tr/wpsend/icons/word.png",shortFileName)
        elif(fileExtension == "rar" or fileExtension == "zip" or fileExtension == "gz"):
            htmlCode = htmlCode.format("http://furkanyolal.com.tr/wpsend/icons/winrar.png",shortFileName)
        
        else:
            htmlCode = htmlCode.format("http://furkanyolal.com.tr/wpsend/icons/default.png",shortFileName)

    elif(kind == "message"):
        htmlCode = """
        <div class="message sent">
            {}
            <span class="metadata">
                <span class="time"></span><span class="tick"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg></span>
            </span>
        </div>"""
        src = src.replace("\n","<br>")
        htmlCode = htmlCode.replace("\n","").replace("\r","").format(src)
    elif(kind == "image"):
        htmlCode = """
        <div class="message sent">
                  <img src="{}" width="240" style="border-radius:5px;">
                  <span class="metadata">
                      <span class="time"></span><span class="tick"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg></span>
                  </span>
                </div>
        """
        htmlCode = htmlCode.format(urllib.parse.quote_plus(src)).replace("\\","/").replace("\n","").replace("\r","")
    return htmlCode