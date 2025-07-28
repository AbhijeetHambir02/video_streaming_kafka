import React from "react";

const VideoCard = ({ video, streamUrl }) => {
    return (
        <div>
            <video
                width="80%"
                height="70%"
                controls
                src={streamUrl}
            />
            <div className="video-info">
                <h4 className="file-name">{video.file_name}</h4>
                {/* <span className="upload-date">
                    Uploaded on {new Date(video.uploaded_at).toLocaleString()}
                </span> */}
            </div>
        </div>
    );
};

export default VideoCard;
