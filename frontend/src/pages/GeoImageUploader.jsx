import React, { useState } from 'react';
import EXIF from 'exif-js';

const ImageUploader = ({ onLocationFound }) => {
  const [imageSrc, setImageSrc] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // 1. 이미지 미리보기
      setImageSrc(URL.createObjectURL(file));

      // 2. EXIF 데이터에서 GPS 추출
      EXIF.getData(file, function () {
        const latData = EXIF.getTag(this, "GPSLatitude");
        const lonData = EXIF.getTag(this, "GPSLongitude");
        const latRef = EXIF.getTag(this, "GPSLatitudeRef"); // N or S
        const lonRef = EXIF.getTag(this, "GPSLongitudeRef"); // E or W

        if (latData && lonData) {
          // 도/분/초(DMS) 포맷을 십진수(Decimal)로 변환하는 함수
          const toDecimal = (coord, ref) => {
            let decimal = coord[0] + coord[1] / 60 + coord[2] / 3600;
            if (ref === "S" || ref === "W") decimal *= -1;
            return decimal;
          };

          const latitude = toDecimal(latData, latRef);
          const longitude = toDecimal(lonData, lonRef);

          console.log("📍 사진 위치:", latitude, longitude);
          
          // 부모 컴포넌트로 좌표 전달 (게임 생성용)
          onLocationFound({ lat: latitude, lng: longitude });
        } else {
          alert("❌ 이 사진에는 위치 정보(GPS)가 없습니다!");
        }
      });
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      {imageSrc && <img src={imageSrc} alt="Preview" style={{ width: '200px' }} />}
    </div>
  );
};

export default ImageUploader;